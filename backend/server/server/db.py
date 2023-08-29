from typing import *
from log import logging as log
import pymongo
from pymongo.collection import Collection
import gridfs
from gridfs import GridFS

#ONLY DEV!
MONGO_CFG: Dict = dict(
    host = 'localhost',
    port = 27017,
    username = 'linqua_db_admin',
    password = 'dev_password'
)

class DataBase:
    TIME_FORMAT: str = "%d.%m.%Y, %H:%M:%S"
    def __init__(self) -> None:
        try:
            self.__mongo_db = pymongo.MongoClient(**MONGO_CFG)['linqua']
            self.user: Collection = self.__mongo_db['user']
            self.task: Collection = self.__mongo_db['task']
            self.tmp: Collection = self.__mongo_db['tmp']
            self.files: GridFS = gridfs.GridFS(self.__mongo_db)
        except Exception as e:
            log.error('error connecting to database')
            log.debug(e)

db = DataBase()