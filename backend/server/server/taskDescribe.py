from typing import *
from task import Task
from speech import Speech, GrammarError, WordPresent
from pydantic import BaseModel
import base64


class DescribeTaskReport(BaseModel):
    text: str
    words: List[str]
    score_length: int
    score_hitword: int
    score_grammar: int
    grammar_errors: List[GrammarError]
    hitwords_used: List[WordPresent]

class DescribeTaskInfo(BaseModel):
    taskid: str
    text: str
    b64image: Optional[str] = None

class DescribeTask(Task):
    TASK_TYPE = 'DESCRIBE'
    def __init__(self, id: str) -> None:
        super().__init__(id)
        self.image_id: str = self._task_data['image_id']
        self.text: str = self._task_data['text']
        self.word_count_min: int = self._task_data['word_count_min']
        self.word_count_best: int = self._task_data['word_count_best']
        self.hitwords: List[str] = self._task_data['hitwords']
        self.hitwords_used: List[WordPresent] = []
        self.grammar_errors: List[GrammarError] = []
        self.score_length: int = 0
        self.score_hitword: int = 0
        self.score_grammar: int = 0

    @property
    def imageb64(self) -> Optional[str]:
        if self.image_id != None:
            img = Task.file_db.get(self.image_id).read()
            return base64.b64encode(img).decode('utf-8')
        return None
        
    def solve(self, speech: Speech) -> DescribeTaskReport:
        self.solution: Speech = speech
        self.grammar_errors = self.solution.grammar
        self.hitwords_used = self.solution.has_words(self.hitwords)
        self._calc_score()
        return DescribeTaskReport(
            text = self.solution.text,
            words = self.solution.words,
            score_length=self.score_length,
            score_hitword=self.score_hitword,
            score_grammar=self.score_grammar,
            grammar_errors=self.grammar_errors,
            hitwords_used=self.hitwords_used
            )
    
    @property
    def overview(self) -> DescribeTaskInfo:
         return DescribeTaskInfo(
             taskid = self.id,
             text = self.text,
             b64image = self.imageb64
         )
    
    def _calc_score(self):
        #LENGTH #Score is between 0 and 100
        if (words_above_min := self.solution.word_count-self.word_count_min) <= 0:
            self.score_length = 0
        elif (word_range := self.word_count_best - self.word_count_min) <= words_above_min:
            self.score_length = 100
        else: 
            self.score_length = int(100 * words_above_min / word_range)

        #HITWORDS #Score is between 0 and 100
        hits = 0
        for used_word in self.hitwords_used:
            hits += 1 if used_word.present else 0
        self.score_hitword = int(100 * hits / len(self.hitwords))

        #GRAMMAR #Score is between 0 and 100
        self.score_grammar = 0 if len(self.grammar_errors) > 0 else 100

    
    @staticmethod
    def create(text: str, word_count_min: int, word_count_best: int, hitwords: List[str] = [], image: bytes = None, creator: str = None) -> str:
        return super().create(
            creator = creator, 
            task_type = DescribeTask.TASK_TYPE, 
            task_attribs = dict(
                image_id = str(Task.file_db.put(image)) if isinstance(image, bytes) else None,
                text = text,
                word_count_min = word_count_min,
                word_count_best = word_count_best,
                hitwords = hitwords,
            ))
    
    def delete(self) -> bool:
        if self.image_id != None:
            Task.file_db.delete(self.image_id)
        return super().delete()