from __future__ import annotations
from typing import *
from functools import wraps
from fastapi import Request, Response
from uuid import uuid4
from datetime import datetime, timedelta

# Allgemeine Anmerkungen zu Session
# Die Benutzersessions werden ausschließlich im Arbeitsspeicher gehalten, werden also bei einem Neustart der Anwendung automatisch zurückgesetzt
# Derzeut besteht noch keine automatische Bereinigung, Pro Benutzer ist also immer ein Eintrag aktiv -> müsste für Produktivzustand geändert werden

#TODO:
# - SESSION GARBAGE COLLECTION (remove unuse session after time)



#SETTINGS:
_SESSION_DURATION: int = 30 #Dauer Wie lange eine Session ihre gültigkeit behält (wird nicht gelöscht danach, sondern nur ungültig!)
_SESSION_COOKIE_KEY: str = 'LINQUA_SESSION' #Name des Sessioncookies unter welchem die Sessions abgelegt werden.

class Session:
    """Klasse um eine einzelne Benutzer Session zu verwalten
    """
    def __init__(self, userid: str) -> Session:
        """Konstruktor zum erzeugen einer Session

        :param userid: id des Benutzers für welchen eine Session angelegt werden soll
        :type userid: str
        :return: Session Objekt
        :rtype: Session
        """
        self.id: str = f's_{uuid4().hex}'
        self.userid: str = userid
        self.created: datetime = datetime.now()
        self.expires: datetime = self.created + timedelta(minutes=_SESSION_DURATION)
    
    @property
    def sconds_until_expiry(self) -> int:
        """Zeit in Sekunden bis die Session ungültig wird

        :return: Sekunden bis zum Ablauf der Session
        :rtype: int
        """
        return int((self.expires - datetime.now()).total_seconds())
    
    @property
    def is_valid(self) -> bool:
        """Gibt an ob die Session noch gültig ist (noch nicht abgelaufen)

        :return: Session noch gültig (Ja/Nein)
        :rtype: bool
        """
        return self.sconds_until_expiry > 0

    def renew(self):
        """Erneueren einer Session (setzen der Ablaufzeit auf Initialwert)
        """
        self.expires: datetime = datetime.now() + timedelta(minutes=_SESSION_DURATION)

    @staticmethod
    def of_request(request: Request) -> Session:
        """Liefert die zueghörige Session zu einem Request (wird aus Sessioncookie extrahiert)

        :param request: FastAPI Request Objekt
        :type request: Request
        :return: Session des Benutzers des Requtests
        :rtype: Session
        """
        return request.__getattribute__('linqua_session')
    
    def start(self) -> Response:
        """Startet eine Session (ergänzt die Anweisung zum setzten Session Cookie)

        :return: Response(FastAPI)
        :rtype: Response
        """
        response: Response = Response()
        response.set_cookie(_SESSION_COOKIE_KEY, sessions.start_session(self.userid).id, max_age=Session.sconds_until_expiry, httponly=True)
        return response
    
    def destroy(self) -> Response:
        """Beendet eine Session (löscht diese aus dem Arbeitsspeicher und ergänzt die Anweisung zum löschen des Session Cookies)

        :return: Response (FastAPI)
        :rtype: Response
        """
        if sessions.remove_session(self.id):
            response: Response = Response('session has ended')
            response.delete_cookie(_SESSION_COOKIE_KEY, httponly=True)
            return response
        return Response('no session to end')
    
    

class Sessions:
    """Klasse um die Summe aller Benutzersessions zu verwalten
    """
    __sessions: Dict[str, Session] = {}
    def start_session(self, userid: str) -> Session:
        """Erzeugt eine Session und fügt diese zu den aktiven Sessions hinzu (Arbeitsspeicher)

        :param userid: id des Benutzers
        :type userid: str
        :return: Session Objekt
        :rtype: Session
        """
        if existing_session := self.get_session(userid=userid):
            existing_session.renew()
            return existing_session
        new_session: Session = Session(userid)
        self.__sessions[new_session.id] = new_session
        return new_session

    def get_session(self, id: Optional[str] = None,  userid: Optional[str] = None) -> Optional[Session]:
        """Liefert das zu einer BenutzerID ODER SessionID zugehörige Session Objekt

        :param id: ID einer Session, defaults to None
        :type id: Optional[str], optional
        :param userid: ID eines Benutzers, defaults to None
        :type userid: Optional[str], optional
        :return: Session Objekt wenn verfügbar
        :rtype: Optional[Session]
        """
        if id:
            return self.__sessions.get(id)
        elif userid:
            for session in self.__sessions.values():
                if session.userid == userid:
                    return session
        return None
    
    def remove_session(self, id: str) -> bool:
        """Entfernt eine Session von den aktiven Sessions

        :param id: id der Session
        :type id: str
        :return: True wenn die Session existierte und entfernt wurde, False wenn keine Session zu den IDs gefunden wurde
        :rtype: bool
        """
        return self.__sessions.pop(id, None) != None


sessions: Sessions = Sessions()
def session_required(fnc):
    """FastAPI Endpunkt Dekorator um automatierst zu Prüfen ob eine Session vorhanden ist (auslesen des Sessioncookies und Prüfen auf Gültigkeit)

    :param fnc: Endpunkt Funktion (wird durch decorator "@" übergeben)
    :type fnc: Callable (Funktion)
    :return: Response (FastAPI)
    :rtype: Response
    """
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
