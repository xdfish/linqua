from typing import *
from log import logging as log
import pymongo
import gridfs

#ONLY DEV!
MONGO_CFG: Dict = dict(
    host = 'localhost',
    port = 27017,
    username = 'admin',
    password = 'password'
)

TIME_FORMAT: str = "%d.%m.%Y, %H:%M:%S"

class DataBase:
    def __init__(self) -> None:
        try:
            self.__mongo_db = pymongo.MongoClient(**MONGO_CFG)['linqua']
            self.user = self.__mongo_db['user']
            self.task = self.__mongo_db['task']
            self.files = gridfs.GridFS(self.__mongo_db)
        except Exception as e:
            log.error('error connecting to database')
            log.debug(e)

db = DataBase()