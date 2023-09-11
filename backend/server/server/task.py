from typing import *
from exceptions import LinquaExceptions
from bson.objectid import ObjectId
from db import db, Collection, GridFS
import random
from datetime import datetime


class Task:
    """Grundklasse aller Aufgaben (stellt grundlegende Funktionen zur Verfügung, welche für alle Aufgaben gültigkeit haben)

    :raises LinquaExceptions.TaskUnknown: Ausnahme wenn eine ID (siehe Konstruktor) keiner Aufgabe zugeordnet werden kann
    :raises LinquaExceptions.WrongTaskClass: Ausnahme wenn eine falsche Aufgabenklasse zum Initialisieren verwendet wurde
    """
    TASK_TYPE: str = None     #REQUIRED FOR SUBCLASSES!
    TIME_FORMAT: str = db.TIME_FORMAT

    file_db: GridFS = db.files
    tmp_storage: Collection = db.tmp
    db: Collection = db.task
    
    def __init__(self, id: str) -> None:
        """Konstruktor um ein Aufgabenobjekt zu erzeugen

        :param id: Aufgaben ID
        :type id: str
        :raises LinquaExceptions.TaskUnknown: SIEHE KLASSENDEFINITION
        :raises LinquaExceptions.WrongTaskClass: SIEHE KLASSENDEFINITION
        """
        self.__task_data = Task.db.find_one({'_id': ObjectId(id)})
        if not self._task_data:
            raise LinquaExceptions.TaskUnknown(f'unkown Task with id: {id}')
        if self.TASK_TYPE:
            if not self._task_data['task_type'] == self.TASK_TYPE:
                raise LinquaExceptions.WrongTaskClass(f'task with id {id} is not type "{self.TASK_TYPE}"')
    
    @property
    def _task_data(self) -> Dict:
        """Liefert die Daten der Aufgabe

        :return: Daten der Aufgabe
        :rtype: Dict
        """
        return self.__task_data

    @property
    def creator(self) -> str:
        """Liefert Erzeuger (Benutzer) der Aufgabe

        :return: _description_
        :rtype: str
        """
        return self._task_data.get('creator')
    
    @property
    def created(self) -> str:
        """Liefert das Datum wann die Aufgabe erzeugt wurde

        :return: Datum in Textform
        :rtype: str
        """
        return self._task_data.get('created')
    
    @property
    def id(self) -> str:
        """Liefert die ID der Aufgabe

        :return: Aufgaben ID
        :rtype: str
        """
        return str(self.objectId)
    
    @property
    def objectId(self) -> ObjectId:
        """Datenbank Objekt ID zur Speicherung (MongoDB) der Aufgabe

        :return: Datenbank ID
        :rtype: ObjectId
        """
        return self._task_data['_id']
    
    @property
    def overview(self):
        """Übersicht der Aufgabe (muss in den spezifischen Aufgaben implementiert werden)
        """
        # relevant information for the user to solve the task
        ...

    def solve(self):
        """Löst eine Aufgabe (muss in den spezifischen Aufgaben implementiert werden)
        """
        # called to solve the task
        ...

    @staticmethod
    def create(task_type: str, task_attribs: Dict = {}, creator: str = None) -> str:
        """Erzeugt eine neue Aufgabe (und speichet sie in DB)

        :param task_type: _description_
        :type task_type: str
        :param task_attribs: _description_, defaults to {}
        :type task_attribs: Dict, optional
        :param creator: _description_, defaults to None
        :type creator: str, optional
        :return: _description_
        :rtype: str
        """
        # create a new task
        task_attribs['creator'] = creator
        task_attribs['created'] = datetime.now().strftime(db.TIME_FORMAT)
        task_attribs['task_type'] = task_type
        return str(Task.db.insert_one(task_attribs).inserted_id)
    
    def delete(self) -> bool:
        """Löscht die Aufgabe aus der Datenbank

        :return: Erfolg (Ja/Nein)
        :rtype: bool
        """
        # delete existing task
        return Task.db.delete_one({'_id': self.objectId}).deleted_count > 0
    

    #TASKS METHOD ----
    @classmethod
    def get_random_id(cls, exclude_ids: List[str]) -> str:
        """Liefert eine Zufällige Aufgaben ID

        :param exclude_ids: IDs welche nicht berücksicht werden sollen
        :type exclude_ids: List[str]
        :return: Aufgaben ID
        :rtype: str
        """
        tasks: List[Task] = [str(task['_id']) for task in Task.db.find({'task_type': cls.TASK_TYPE, '_id': { '$nin' : [ObjectId(id) for id in exclude_ids]}}, {'_id': 1})]
        if len(tasks) > 0:
            return random.choice(tasks)
        return None
    
    @classmethod
    def list(cls) -> List[str]:
        """Liefert eine Liste aller Aufgaben (ids)

        :return: Aufgaben ID Liste
        :rtype: List[str]
        """
        task_filter = {'task_type': cls.TASK_TYPE} if cls.TASK_TYPE else {}
        tasks =  [str(task['_id']) for task in Task.db.find(task_filter, {'_id': 1})]
        tasks.sort()
        return tasks
