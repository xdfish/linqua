from typing import *
from exceptions import LinquaExceptions
from bson.objectid import ObjectId
from db import db, Collection, GridFS
import random
from datetime import datetime

class Task:
    TASK_TYPE: str      #REQUIRED FOR SUBCLASSES!
    __db_data: Dict     #WILL BE SET WHILE INIT

    file_db: GridFS = db.files
    db: Collection = db.task

    def __init__(self, id: str) -> None:
        self.__db_data = Task.db.find_one({'_id': ObjectId(id)})
        if not self.__db_data:
            raise LinquaExceptions.TaskUnknown(f'unkown Task with id: {id}')
        if not self.__db_data['task_type'] == self.TASK_TYPE:
            raise LinquaExceptions.WrongTaskClass(f'task with id {id} is not type "{self.TASK_TYPE}"')

    @property
    def creator(self) -> str:
        return self.__db_data.get('creator')
    
    @property
    def created(self) -> str:
        return self.__db_data.get('created')
    
    @property
    def id(self) -> str:
        return self.__db_data['id']
    
    @property
    def objectId(self) -> ObjectId:
        return ObjectId(self.id)
    
    @property
    def overview(self):
        # relevant information for the user to solve the task
        ...

    def solve(self):
        # called to solve the task
        ...

    @staticmethod
    def create(task_type: str, task_attribs: Dict = {}, creator: str = None) -> str:
        # create a new task
        task_attribs['creator'] = creator
        task_attribs['created'] = datetime.now().strftime(db.TIME_FORMAT)
        task_attribs['task_type'] = task_type
        return Task.db.insert_one(task_attribs).inserted_id
    
    def delete(self) -> bool:
        # delete existing task
        return Task.db.delete_one({'_id': self.objectId}).deleted_count > 0
    
    @classmethod
    def get_random_id(cls, exclude_ids: List[str]):
        tasks: List[Task] = [str(task['_id']) for task in Task.db.find({'task_type': cls.TASK_TYPE, '_id': { '$nin' : [ObjectId(id) for id in exclude_ids]}}, {'_id': 1})]
        if len(tasks) > 0:
            return random.choice(tasks)
        return None
    
    @classmethod
    def list(cls) -> List[str]:
        task_filter = {'task_type': cls.TASK_TYPE} if cls.TASK_TYPE else {}
        tasks =  [str(task['_id']) for task in Task.db.find(task_filter, {'_id': 1})]
        tasks.sort()
        return tasks
