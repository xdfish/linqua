from fastapi import FastAPI, Form, Request, Response, UploadFile, File, APIRouter
from session import session_required
from user import SessionUser, User
from task import Task, DescribeTask
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
def task_add(request: Request, info: str = Form(None), image: UploadFile = File(None)):
   user = SessionUser(request)
   imgage_data: bytes = image.file.read() if image else None
   info: Dict = json.loads(info)
   Task = DescribeTask.create(image=imgage_data, creator=user.id, **info)
   return Task.info

@api.post('/task/random')
@session_required
def task_random(request: Request, exclude_ids: str = Form(None)):
   exclude_ids: List[str] = json.loads(exclude_ids) if exclude_ids else []
   if randId := DescribeTask.get_random_id(exclude_ids):
      return DescribeTask(randId).info
   return Response('no tasks left', 400)

@api.get('/task/list')
@session_required
def task_list(request: Request):
   return DescribeTask.list()

@api.post('/task/delete')
@session_required
def task_delete(request: Request, id: str = Form(...)):
   task = DescribeTask(id)
   return task.delete()

@api.post('/task/solve')
@session_required
def task_solve(request: Request, id: str = Form(...), record: UploadFile = File(...)):
   task = DescribeTask(id)
   solution = task.solve(Speech(record.file.read(), record.filename.split('.')[-1]))
   print(solution)
   return solution

#ADMIN ONLY
#TODO
class UserFNC(Enum):
    create = 'create'
    delete = 'delete'
    update = 'update'

#create user, tasks etc.