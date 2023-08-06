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

class User():
    def __init__(self, id: str = None, username: str = None) -> None:
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
        return self.password_salt_hash[:32]

    @property
    def password_hash(self) -> str:
        return self.password_salt_hash[32:]

    @staticmethod
    def create(username: str, password: str, first_name: str, last_name: str, email: str, role: Literal['ADMIN', 'USER']) -> User:
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

    def update(self):
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
        return db.user.delete_one({'_id': ObjectId(self.id)}).deleted_count > 0
    
    def validate_credentials(self, password: str) -> bool:
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self.password_salt, 100000) == self.password_hash
    

class SessionUser(User):
    def __init__(self, request: Optional[Request] = None) -> None:
        self.session: Session = Session.of_request(request)
        super().__init__(id = self.session.userid)
    
    @staticmethod
    def start_session(userid):
        return Session(userid).start()

#u = User.create('testuser', 'password', 'testuser', 'usertest', 'test@test.test', 'ADMIN')