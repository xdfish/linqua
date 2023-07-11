from fastapi import FastAPI, Form, Request, Response, UploadFile, File
from session import session_required
from user import SessionUser, User
from taskDescribe import DescribeTask
from taskTalk import TalkTask
from task import Task
from enum import Enum
from typing import *
from exceptions import LinquaExceptions
from basemodels import *
from speech import Speech
import json
from fastapi.staticfiles import StaticFiles



app = FastAPI()
api = FastAPI()
app.mount('/api', api)

app.mount("/", StaticFiles(directory="www", html = True), name="static")

@api.post('/login')
def login(request: Request, username: str = Form(...), password: str = Form(...)):
   try:
      user = User(username = username)
      if user.validate_credentials(password):
         return SessionUser.start_session(user.id)
      return Response('wrong password', 401)
   except LinquaExceptions.UserUnknown:
      return Response('unknown user', 401)

@api.post('/logout')
@session_required
def logout(request: Request):
   return SessionUser(request).session.destroy()

@api.get('/user', response_model=UserInfo)
@session_required
def user_info(request: Request) -> UserInfo:
   user = SessionUser(request)
   return UserInfo(**user.__dict__)

@api.post('/task/add')
@session_required
def task_add(request: Request, task_type: str = Form(...), task_data: str = Form(...), image: UploadFile = File(None)):
   user = SessionUser(request)
   imgage_data: bytes = image.file.read() if image else None
   task_data: Dict = json.loads(task_data)
   if task_type == 'DESCRIBE':
      return DescribeTask.create(image=imgage_data, creator=user.id, **task_data)
   elif task_type == 'TALK':
      return TalkTask.create(creator=user.id, **task_data)
   return Response('unkknown task_type', 400)

@api.post('/task/random')
@session_required
def task_random(request: Request, task_type: str = Form(...), exclude_ids: str = Form(None)):
   exclude_ids: List[str] = json.loads(exclude_ids) if exclude_ids else []
   print(task_type)
   if task_type == 'DESCRIBE':
      if randId := DescribeTask.get_random_id(exclude_ids):
         return DescribeTask(randId).overview
   elif task_type == 'TALK':
      if randId := TalkTask.get_random_id(exclude_ids):
         return TalkTask(randId).overview
   return Response('no tasks left', 400)

@api.get('/task/list')
@session_required
def task_list(request: Request):
   return Task.list()

@api.post('/task/delete')
@session_required
def task_delete(request: Request, id: str = Form(...)):
   task = Task(id)
   return task.delete()

@api.post('/task/solve')
@session_required
def task_solve(request: Request, id: str = Form(...), task_type: str = Form(...), record: UploadFile = File(...)):
   if task_type == 'DESCRIBE':
      task = DescribeTask(id)
   elif task_type == 'TALK':
      task = TalkTask(id)
   solution = task.solve(Speech(record.file.read(), record.filename.split('.')[-1]))
   return solution

#ADMIN ONLY
#TODO
class UserFNC(Enum):
    create = 'create'
    delete = 'delete'
    update = 'update'

#create user, tasks etc.