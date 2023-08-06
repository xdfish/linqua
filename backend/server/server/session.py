from __future__ import annotations
from typing import *
from functools import wraps
from fastapi import Request, Response
from uuid import uuid4
from datetime import datetime, timedelta
#Sessions are only in memory

#TODO:
# - SESSION GARBAGE COLLECTION (remove unuse session after time)

#SETTINGS:
_SESSION_DURATION: int = 30 #minutes
_SESSION_COOKIE_KEY: str = 'LINQUA_SESSION'

class Session:
    def __init__(self, userid: str) -> Session:
        self.id: str = f's_{uuid4().hex}'
        self.userid: str = userid
        self.created: datetime = datetime.now()
        self.expires: datetime = self.created + timedelta(minutes=_SESSION_DURATION)
    
    @property
    def sconds_until_expiry(self) -> int:
        return int((self.expires - datetime.now()).total_seconds())
    
    @property
    def is_valid(self) -> bool:
        return self.sconds_until_expiry > 0

    def renew(self):
        self.expires: datetime = datetime.now() + timedelta(minutes=_SESSION_DURATION)

    @staticmethod
    def of_request(request: Request) -> Session:
        return request.__getattribute__('linqua_session')
    
    def start(self) -> Response:
        response: Response = Response()
        response.set_cookie(_SESSION_COOKIE_KEY, sessions.start_session(self.userid).id, max_age=Session.sconds_until_expiry, httponly=True)
        return response
    
    def destroy(self) -> Response:
        if sessions.remove_session(self.id):
            response: Response = Response('session has ended')
            response.delete_cookie(_SESSION_COOKIE_KEY, httponly=True)
            return response
        return Response('no session to end')
    
    

class Sessions:
    __sessions: Dict[str, Session] = {}
    def start_session(self, userid: str) -> Session:
        if existing_session := self.get_session(userid=userid):
            existing_session.renew()
            return existing_session
        new_session: Session = Session(userid)
        self.__sessions[new_session.id] = new_session
        return new_session

    def get_session(self, id: Optional[str] = None,  userid: Optional[str] = None, renew_session: bool = True) -> Optional[Session]:
        if id:
            return self.__sessions.get(id)
        elif userid:
            for session in self.__sessions.values():
                if session.userid == userid:
                    return session
        return None
    
    def remove_session(self, id: str) -> bool:
        return self.__sessions.pop(id, None) != None


sessions: Sessions = Sessions()
def session_required(fnc):
    @wraps(fnc)
    def decorator(request: Request, *args, **kwargs):
        if session_id := request.cookies.get(_SESSION_COOKIE_KEY):
            if session := sessions.get_session(id=session_id):
                if session.is_valid:
                    session.renew()
                    request.__setattr__('linqua_session', session)
                    return fnc(request, *args, **kwargs)
                return Response('session expired', 440)
        return Response('no login', 401)
    return decorator
