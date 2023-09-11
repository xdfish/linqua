from fastapi import FastAPI, Form, Request, Response, UploadFile, File
from session import session_required
from user import SessionUser, User, admin_init
from taskDescribe import DescribeTask, DescribeTaskReport
from taskTalk import TalkTask, TaskTalkReport
from taskTalkAuto import TalkAutoTask
from task import Task
from enum import Enum
from typing import *
from exceptions import LinquaExceptions
from basemodels import *
from speech import Speech
import json, pathlib
from fastapi.staticfiles import StaticFiles
from words import Words


app = FastAPI()
api = FastAPI()
app.mount('/api', api)

#Initialisieren der Adminfunktionen (aktuell nur erzeugen des Admin Benutzers)
admin_init()

#Erzeugen des Resource Orders (wwww) sollte er nicht existieren
pathlib.Path('./www').mkdir(exist_ok=True)

#Order www für die statischen Dateien festlegen
app.mount("/", StaticFiles(directory="www", html = True), name="static")


#Login Endpunkt
@api.post('/login')
def login(request: Request, username: str = Form(...), password: str = Form(...)) -> Response:
   """Endpunkt um einen Login (starten einer Benutzersession) durchzuführen

   :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt)
   :type request: Request
   :param username: Benutzername, defaults to Form(...)
   :type username: str, optional
   :param password: Passwort, defaults to Form(...)
   :type password: str, optional
   :return: Response (FastAPI)
   :rtype: Response
   """
   try:
      user = User(username = username)
      if user.validate_credentials(password):
         return SessionUser.start_session(user.id)
      return Response('wrong password', 401)
   except LinquaExceptions.UserUnknown:
      return Response('unknown user', 401)


#Logout Endpunkt
@api.post('/logout')
@session_required
def logout(request: Request) -> Response:
   """Endpunkt um einen logout (beenden der aktuellen Benutzersession) durchzuführen

   :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt)
   :type request: Request
   :return: Response (FastAPI)
   :rtype: Response
   """
   return SessionUser(request).session.destroy()

@api.get('/user', response_model=UserInfo)
@session_required
def user_info(request: Request) -> UserInfo:
   """Endpunkt um Benutzerinformationen abzurufen (der aktuellen Session)

   :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt)
   :type request: Request
   :return: Response (FastAPI)
   :rtype: UserInfo
   """
   user = SessionUser(request)
   return UserInfo(**user.__dict__)


#Endpunkt zum hinzufügen von neuen Aufgaben
@api.post('/task/add')
@session_required
def task_add(request: Request, task_type: str = Form(...), task_data: str = Form(...), image: UploadFile = File(None)) -> Response:
   """Endpunkt um eine neue Aufgabe eines bestimmten typs anzulegen

   :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt)
   :type request: Request
   :param task_type: Aufgaben Typ, defaults to Form(...)
   :type task_type: str, optional
   :param task_data: Daten der Aufgabe, defaults to Form(...)
   :type task_data: str (serialized Dict), optional
   :param image: Zu der Aufgabe zugehörige Bilder, defaults to File(None)
   :type image: UploadFile, optional
   :return: Response (FastAPI)
   :rtype: Response
   """
   user = SessionUser(request)
   imgage_data: bytes = image.file.read() if image else None
   task_data: Dict = json.loads(task_data)
   if task_type == 'DESCRIBE':
      return DescribeTask.create(image=imgage_data, creator=user.id, **task_data)
   elif task_type == 'TALK':
      return TalkTask.create(creator=user.id, **task_data)
   elif task_type == 'TALK-AUTOGEN':
      return TalkAutoTask.create(creator=user.id, **task_data)
   return Response('unkknown task_type', 400)


@api.post('/task/random')
@session_required
def task_random(request: Request, task_type: str = Form(...), exclude_ids: str = Form(None), auto_data: str = Form(None)) -> Response:
   """Endpunkt um eine zufällige Aufgabe zu erhalten

   :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt)
   :type request: Request
   :param task_type: Aufgaben Typ, defaults to Form(...)
   :type task_type: str, optional
   :param exclude_ids: ids der Aufgaben welche in der zufälligen Auswahl nicht berücksicht werden sollen, defaults to Form(None)
   :type exclude_ids: str (serialized List), optional
   :param auto_data: Für den Aufgabentyp "AUTO GEN" spezifische konfigurations Parameter (min_freq und max_freq), defaults to Form(None)
   :type auto_data: str (serialized Dict), optional
   :return: Response (FastAPI)
   :rtype: Response
   """
   exclude_ids: List[str] = json.loads(exclude_ids) if exclude_ids else []
   auto_data: Dict[str: Any] = json.loads(auto_data) if auto_data else {}
   if task_type == 'DESCRIBE':
      if randId := DescribeTask.get_random_id(exclude_ids):
         return DescribeTask(randId).overview
   elif task_type == 'TALK':
      if randId := TalkTask.get_random_id(exclude_ids):
         return TalkTask(randId).overview
   elif task_type == 'TALK-AUTOGEN':
      if randId := TalkAutoTask.get_random_id([]):
         return TalkAutoTask(randId).generate(auto_data.get('min_freq'), auto_data.get('max_freq'))
   return Response('no tasks left', 400)

#Endpunkt
@api.get('/task/list')
@session_required
def task_list(request: Request) -> Response:
   """Endpunkt um eine Liste aller verfügbaren Aufgaben abzurufen

   :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt)
   :type request: Request
   :return: Liste der Aufgaben IDs (unique)
   :rtype: List[str]
   """
   return Task.list()

@api.post('/task/delete')
@session_required
def task_delete(request: Request, id: str = Form(...)) -> Response:
   """Endpunkt um eine Aufgabe zu löschen

   :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt)
   :type request: Request
   :param id: Aufgaben ID, defaults to Form(...)
   :type id: str, optional
   :return: Response (FastAPI)
   :rtype: Response
   """
   task = Task(id)
   return task.delete()

@api.post('/task/solve')
@session_required
def task_solve(request: Request, id: str = Form(...), task_type: str = Form(...), record: UploadFile = File(...), tmpid: str = Form(None)) -> Response:   
   """Endpunkt um eine Aufgabe zu lösen

   :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt)
   :type request: Request
   :param id: Aufgaben ID (der Aufgabe die gelöst werden soll), defaults to Form(...)
   :type id: str, optional
   :param task_type: Aufgaben Typ (der Aufgabe die gelöst werden soll), defaults to Form(...)
   :type task_type: str, optional
   :param record: Audiodatei der Spracheingabe, defaults to File(...)
   :type record: UploadFile, optional
   :param tmpid: Für den Aufgabentyp "AUTO GEN" spezfische id, zum zuordnen der temporären Aufgaben Daten, defaults to Form(None)
   :type tmpid: str, optional
   :return: Response
   :rtype: Union[TaskTalkReport, DescribeTaskReport]
   """
   if task_type == 'DESCRIBE':
      task = DescribeTask(id)
   elif task_type == 'TALK':
      task = TalkTask(id)
   elif task_type == 'TALK-AUTOGEN':
      task = TalkAutoTask(id)
      return task.solve(Speech(record.file.read(), record.filename.split('.')[-1]), tmpid)
   return task.solve(Speech(record.file.read(), record.filename.split('.')[-1]))


@api.post('/words/update')
@session_required
def word_upadte(request: Request, data: UploadFile = File(...)) -> Response:
   """Endpunkt zum anlegen/updaten der Wortdatenbank

   :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt)
   :type request: Request
   :param data: Daten zum generieren der Wortdatenbank (.xslx SUBTLEX), defaults to File(...)
   :type data: UploadFile, optional
   :return: Response (FastAPI)
   :rtype: Response
   """
   if not data.filename.split('.xlsx'):
      return Response('SUBTLEX words file has to be .xlsx', 400)
   return Response(json.dumps({'msg':'ok'})) if Words.update(data.file.read()) else Response('error updating word database') 

@api.get('/words/classes')
@session_required
def word_classes(request: Request) -> Response:
   """Endpunkt um die verfügbaren Wortklassen der Wortdatenbank abzurufen

   :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt)
   :type request: Request
   :return: Liste der Wortarten
   :rtype: List[str]
   """
   try:
      return Words().classes
   except Exception:
      return []
