from __future__ import annotations
from typing import *
import os, hashlib
from exceptions import LinquaExceptions
import base64
from session import Session
from fastapi import Request
from datetime import datetime
from log import logging as log
from bson.objectid import ObjectId
from db import db

TIME_FORMAT: str = "%d.%m.%Y, %H:%M:%S"

def admin_init():
    """Initialisert den Adminbenutzer
    """
    try:
        User(username='linqua-admin')
    except LinquaExceptions.UserUnknown:
        User.create(uname := 'linqua-admin', upw := 'admin123', 'admin', 'admin', 'admin@admin.admin', 'ADMIN')
        log.debug(f'admin user created: username: {uname}, password: {upw}')

class User():
    """Benutzerobjekt
    """
    def __init__(self, id: str = None, username: str = None) -> None:
        """Konstruktor zum erstellen eines Benutzers (aus id oder benutzername  )

        :param id: Benutzer ID, defaults to None
        :type id: str, optional
        :param username: Benutzername, defaults to None
        :type username: str, optional
        :raises LinquaExceptions.UserUnknown: Ausnahem wenn eine ID oder ein Benutzername keinem Benutzer zugeordnet waren
        """
        user = db.user.find_one({'_id': ObjectId(id)} if id else {'username':username})
        if not user:
            raise LinquaExceptions.UserUnknown(f'user not found!')
        
        self.id: str = str(user['_id'])
        self.username: str = user['username']
        self.password_salt_hash: str = base64.b64decode(user['password_salt_hash'])
        self.first_name = user['first_name']
        self.last_name = user['last_name']
        self.email = user['email']
        self.created = user['created']
        self.role = user['role']

    @property
    def password_salt(self) -> str:
        """Liefert den verwendete Passwort SALT

        :return: verwendeter Passwort SALT
        :rtype: str
        """
        return self.password_salt_hash[:32]

    @property
    def password_hash(self) -> str:
        """Liefert das Passwort verhasht

        :return: gehashtes Passwort
        :rtype: str
        """
        return self.password_salt_hash[32:]

    @staticmethod
    def create(username: str, password: str, first_name: str, last_name: str, email: str, role: Literal['ADMIN', 'USER']) -> User:
        """Erzeugt einen Benutzer (legt diesen in der Datenbank ab)

        :param username: Benutzername
        :type username: str
        :param password: Passwort
        :type password: str
        :param first_name: Vorname des Benutzers
        :type first_name: str
        :param last_name: Nachname des Benutzers
        :type last_name: str
        :param email: Email des Benutzers
        :type email: str
        :param role: Rolle des Benutzers
        :type role: Literal[&#39;ADMIN&#39;, &#39;USER&#39;]
        :raises LinquaExceptions.UserAlreadyExists: Ausnahme wenn ein Benutzer mit dem Benutzernamen bereits existiert
        :return: Benutzerobjekt 
        :rtype: User
        """
        if db.user.find_one({'username':username}, {'_id':0}):
             raise LinquaExceptions.UserAlreadyExists(f'user with "{username}" already exists')

        pwsalt = os.urandom(32)
        hashedpw = pwsalt + hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), pwsalt, 100000)
        
        id = db.user.insert_one(
            dict(
                username = username,
                password_salt_hash = base64.b64encode(hashedpw).decode('ascii'),
                first_name = first_name,
                last_name = last_name,
                email = email,
                created = datetime.now().strftime(TIME_FORMAT),
                role = role
            )).inserted_id
        return User(str(id))

    def update(self) -> bool:
        """Updatet die Informationen eines Benutzers

        :return: Erfolgreich (Ja/Nein)
        :rtype: bool
        """
        return db.user.update_one({'_id': ObjectId(self.id)},{'$set': {
            'username': self.username, 
            'password_salt_hash': self.password_hash, 
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'created': self.created}
            }
        ).matched_count > 0
    
    def delete(self) -> bool:
        """Löscht einen Benutzer

        :return: Erfolgreich (Ja/Nein)
        :rtype: bool
        """
        return db.user.delete_one({'_id': ObjectId(self.id)}).deleted_count > 0
    
    def validate_credentials(self, password: str) -> bool:
        """Prüft Korrektheit des Passworts zum zugehörigen Benutzer

        :param password: Passwort
        :type password: str
        :return: Ist Korrekt (Ja/Nein)
        :rtype: bool
        """
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self.password_salt, 100000) == self.password_hash
    

class SessionUser(User):
    """Session Objekt welches einem konkreten Benutzers zugeordnet wurde

    :param User: Benutzerobjekt
    :type User: User
    """
    def __init__(self, request: Optional[Request] = None) -> None:
        """Kontruktor einer Benutzersession

        :param request: FastAPI spezifischer request parameters (wird für Decorator benötigt), defaults to None
        :type request: Optional[Request], optional
        """
        self.session: Session = Session.of_request(request)
        super().__init__(id = self.session.userid)
    
    @staticmethod
    def start_session(userid: str):
        """Startet eine Session welche einem Benutzer zugeordet ist

        :param userid: Benutzer ID
        :type userid: str
        :return: Session Objekt
        :rtype: Session
        """
        return Session(userid).start()
