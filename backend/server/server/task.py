from typing import *
from speech import Speech
import language_tool_python
from language_tool_python.match import Match
from exceptions import LinquaExceptions
from bson.objectid import ObjectId
from db import db
from datetime import datetime
from pydantic import BaseModel
import base64
import random
import pydub

TIME_FORMAT: str = "%d.%m.%Y, %H:%M:%S"

class Task:
    TASK_TYPE: str
    id: str
    def __init__(self, id: str) -> None:
        ...

    def solve(self):
        ...

    @staticmethod
    def create():
        ...
    
    def delete(self):
        ...
    
    @classmethod
    def get_random_id(cls, exclude_ids: List[str]):
        tasks: List[Task] = [str(task['_id']) for task in db.task.find({'task_type': cls.TASK_TYPE, '_id': { '$nin' : [ObjectId(id) for id in exclude_ids]}}, {'_id': 1})]
        if len(tasks) > 0:
            return random.choice(tasks)
        return None
    
    @classmethod
    def list(cls) -> List[str]:
        task_filter = {'task_type': cls.TASK_TYPE} if cls.TASK_TYPE else {}
        tasks =  [str(task['_id']) for task in db.task.find(task_filter, {'_id': 1})]
        tasks.sort()
        return tasks
    
class GrammarError(BaseModel):
    message: str
    offset: int
    length: int
    suggestion: str

class HitwordsUsed(BaseModel):
    word: str
    used: bool

class DescribeTaskReport(BaseModel):
    text: str
    words: List[str]
    score_length: int
    score_hitword: int
    score_grammar: int
    grammar_errors: List[GrammarError]
    hitwords_used: List[HitwordsUsed]

class DescribeTaskInfo(BaseModel):
    taskid: str
    text: str
    b64image: Optional[str] = None

class DescribeTask(Task):
    TASK_TYPE = 'DESCRIBE'
    grammar_tool = tool = language_tool_python.LanguageTool('en-US')

    def __init__(self, task_id: str) -> None:
        if not (task := db.task.find_one({'_id': ObjectId(task_id)})):
            raise LinquaExceptions.TaskUnknown(f'unkown Task with id: {task_id}')
        if not task['task_type'] == DescribeTask.TASK_TYPE:
            raise LinquaExceptions.WrongTaskClass(f'task with id {task_id} is not type "describe"')
        
        self.id: str = str(task['_id'])
        self.image_id: str = task['image_id']
        self.text: str = task['text']
        self.word_count_min: int = task['word_count_min']
        self.word_count_best: int = task['word_count_best']
        self.hitwords: List[str] = task['hitwords']
        self.hitwords_used: List[HitwordsUsed] = []
        self.grammar_errors: List[GrammarError] = []
        self.score_length: int = 0
        self.score_hitword: int = 0
        self.score_grammar: int = 0

    @property
    def imageb64(self) -> Optional[str]:
        if self.image_id != None:
            img = db.files.get(self.image_id).read()
            return base64.b64encode(img).decode('utf-8')
        return None
        
    def solve(self, speech: Speech) -> DescribeTaskReport:
        self.solution: Speech = speech
        self._check_length()
        self._check_grammar()
        self._check_hitwords()
        return DescribeTaskReport(
            text = self.solution.text,
            words = self.solution.words,
            score_length=self.score_length,
            score_hitword=self.score_hitword,
            score_grammar=self.score_grammar,
            grammar_errors=self.grammar_errors,
            hitwords_used=self.hitwords_used
            )
    
    def info(self) -> DescribeTaskInfo:
         return DescribeTaskInfo(
             taskid = self.id,
             text = self.text,
             b64image = self.imageb64
         )
    
    def _check_length(self): #Score is between 0 and 100
        if (words_above_min := self.solution.word_count-self.word_count_min) <= 0:
            self.score_length = 0
        elif (word_range := self.word_count_best - self.word_count_min) <= words_above_min:
            self.score_length = 100
        else: 
            self.score_length = int(100 * words_above_min / word_range)
    
    def _check_hitwords(self): #Score is between 0 and 100
        words_in_solution: int = 0
        for word in self.hitwords:
            in_solution = word.lower() in self.solution.words
            words_in_solution += 1 if in_solution else 0
            self.hitwords_used.append(HitwordsUsed(
                word = word,
                used = in_solution
            ))
        self.score_hitword = int(100 * words_in_solution / len(self.hitwords))

    def _check_grammar(self): #Score is between 0 and 100
        errors: List[Match] = self.grammar_tool.check(self.solution.text)
        for error in errors:
            if error.category == 'GRAMMAR':
                self.grammar_errors.append(
                    GrammarError(
                        message = error.message,
                        offset = error.offset,
                        length = error.errorLength,
                        suggestion = error.replacements[0] if len(error.replacements) > 0 else ''
                    )
                )
        self.score_grammar = 100 if len(self.grammar_errors) == 0 else 0

    @staticmethod
    def create(text: str, word_count_min: int, word_count_best: int, hitwords: List[str] = [], image: bytes = None, creator: str = None):
        id = db.task.insert_one(
            dict(
                image_id = str(db.files.put(image)) if isinstance(image, bytes) else None,
                text = text,
                task_type = DescribeTask.TASK_TYPE,
                word_count_min = word_count_min,
                word_count_best = word_count_best,
                hitwords = hitwords,
                created = datetime.now().strftime(TIME_FORMAT),
                creator = creator
            )).inserted_id
        return DescribeTask(str(id))
    
    def delete(self) -> bool:
        if self.image_id != None:
            db.files.delete(self.image_id)
        return db.task.delete_one({'_id': ObjectId(self.id)}).deleted_count > 0

