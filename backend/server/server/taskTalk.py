from typing import *
from task import Task
from speech import Speech, WordPresent, GrammarError
from pydantic import BaseModel

class HitwordsUsed(BaseModel):
    """Bewertung eines Hitwords
    """
    word: str
    used: bool

class TaskTalkScore(BaseModel):
    """Score einer Sprachaufgabe

    """
    length: int
    hitwods: int

class TaskTalkReport(BaseModel):
    """Ergebnis einer Sprachaufgaben Lösung
    """
    text_recognized: str
    words_recognized: List[str]
    hitwords_used: List[WordPresent]
    grammar_errors: List[GrammarError]
    score: TaskTalkScore

class TalkTaskInfo(BaseModel):
    """Informationen einer Sprachaufgabe
    """
    taskid: str
    text: str
    hitwords: List[str]
    time_limit: int
    countdown: int
    word_count_min: int
    word_count_max: int
    word_count_best: int

    b64image: Optional[str] = None

class TalkTask(Task):
    """Klasse eine Sprachaufgabe
    """
    TASK_TYPE = 'TALK'

    def __init__(self, id: str) -> None:
        """Konstruktor zum Erzeugen einer Sprachaufgabe

        :param id: Aufgaben ID
        :type id: str
        """
        super().__init__(id)
        self.text = self._task_data['text']
        self.hitwords = self._task_data['hitwords']
        self.word_count_min = self._task_data['word_count_min']
        self.word_count_max = self._task_data['word_count_max']
        self.word_count_best = self._task_data['word_count_best']
        self.time_limit = self._task_data['time_limit']
        self.countdown = self._task_data['countdown']
    
    def solve(self, speech: Speech) -> TaskTalkReport:
        """Löst die Aufgabe (eingabe der Sprachdaten)

        :param speech: Srachdaten in Form einer Speech Klasse
        :type speech: Speech
        :return: Bewertung der Lösung
        :rtype: TaskTalkReport
        """
        self.solution: Speech = speech
        self.hitwords_used = self.solution.has_words(self.hitwords)
        return TaskTalkReport(
            text_recognized = self.solution.text,
            words_recognized = self.solution.words,
            hitwords_used = self.hitwords_used,
            grammar_errors = self.solution.grammar,
            score = self.score
        )

    @property
    def overview(self) -> TalkTaskInfo:
        """Liefert eine Übersicht der Aufgabe (wichtigste Informationen)

        :return: Übersicht der Aufgabe
        :rtype: TalkTaskInfo
        """
        return TalkTaskInfo(
            taskid = self.id,
            text = self.text,
            hitwords = self.hitwords,
            time_limit = self.time_limit,
            countdown = self.countdown,
            word_count_min = self.word_count_min,
            word_count_max = self.word_count_max,
            word_count_best = self.word_count_best
        )

    @property
    def score(self) -> TaskTalkScore:
        """Liefert den Score der beweteten Aufgabe

        :return: Scoreobjekt der Aufgabe
        :rtype: TaskTalkScore
        """
        #HITWORDS
        hits = 0
        for used_word in self.hitwords_used:
            hits += 1 if used_word.present else 0
        score_hitword = int(100 * hits / len(self.hitwords))
        score_length = int(100 if self.solution.word_count > self.word_count_min else 100 * (self.solution.word_count/self.word_count_min))
        return TaskTalkScore(
            length=score_length,
            hitwods=score_hitword
        )

    @staticmethod
    def create(creator: str, text: str, hitwords: List[str], word_count_min: int, word_count_max: int, word_count_best: int, time_limit: int, countdown: int, **kwargs):
        """Erzeugt eine Aufgabe vom Type Sprechen (siehe Konstruktor)

        :param creator: Erzeuger der Aufgabe
        :type creator: str
        :param text: Aufgabentext (stellung)
        :type text: str
        :param hitwords: List mit Hitwörtern die verwendet werden sollen
        :type hitwords: List[str]
        :param word_count_min: Minimale Anzahl an Wörtern (Bewertungm Punkte)
        :type word_count_min: Optional[int]
        :param word_count_max: Maximale Anzahl an Wörter (Bewertung, Abzug wenn überschritten)
        :type word_count_max: int
        :param word_count_best: Gute Anzahl an Wörtern (Bewertung, Bonuspunkte)
        :type word_count_best: Optional[int]
        :param time_limit: Zeitliches Limit (in Sekunden)
        :type time_limit: int
        :param countdown: Zeit des Countdowns
        :type countdown: int
        :return: Aufgabenobjekt
        :rtype: TalkTask
        """
        return super(TalkTask, TalkTask).create(
            creator = creator,
            task_type = TalkTask.TASK_TYPE,
            task_attribs = dict(
                text = text,
                hitwords = hitwords,
                word_count_min = word_count_min,
                word_count_max = word_count_max,
                word_count_best = word_count_best,
                time_limit = time_limit,
                countdown = countdown,
            )
        )