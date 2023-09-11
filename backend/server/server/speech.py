from typing import *
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave, io, json, audioop
from datetime import datetime, timedelta
from wave import Wave_read
from pydub import AudioSegment
import language_tool_python
from language_tool_python.match import Match
from pydantic import BaseModel

SetLogLevel(-1)
MODEL = [
    'model/vosk-model-en-us-0.22',
    'model/vosk-model-en-us-0.42-gigaspeech',           #Best Model         (getestet)
    'model/vosk-model-en-us-daanzu-20200905',           #Fastest Model      (getestet)
    'model/vosk-model-en-us-daanzu-20200905-lgraph'
]


class GrammarError(BaseModel):
    message: str
    offset: int
    length: int
    suggestion: str

class WordPresent(BaseModel):
    word: str
    present: bool


class Speech:
    """Stellt Funktionalitäten bereit um Spracheingaben auszuwerten
    """
    __GRAMMAR_TOOL = language_tool_python.LanguageTool('en-US')     #Instanz des globalen GrammatikTools
    __SPEECH_MODEL = Model(MODEL[1])                                #Sprachmodel um die Spracheingabe in Text umzuwandeln
    time_convert: timedelta                                         #Zeit welche zum Konvertieren der Spracheingabe (audio) benötigt wurde MP3 zu 1CH WAV
    time_analyze: timedelta                                         #Zeit die bnöigt wurde um die 1CH WAV Daten in Text umzuwandeln und alle vorberechnen zu erledigen
    duration: float
    def __init__(self, audio: bytes, audio_type: str = 'wav') -> None:
        """Konstruktor um ein Sprachobjekt zu erstellen

        :param audio: Daten der Audiodatei
        :type audio: bytes
        :param audio_type: Typ der Datei (MP3 oder WAV), defaults to 'wav'
        :type audio_type: str, optional
        """
        self.analyze_result: List[Dict] = []
        self.audio: bytes = audio
        if audio_type == 'mp3':
            audio = self._mp3_to_wav(audio)
        self.wave: Wave_read = self._bytes_to_mono_wav(audio)
        self._analyze_meta()    #0
        self._analyze_text()    #1
        self._analyze_grammar() #2
    
    @property
    def words(self) -> List[str]:
        """Liefert die erkannten Wörter (text)

        :return: Liste mit Wörtern
        :rtype: List[str]
        """
        return [result['word'] for result in self.analyze_result]
    
    @property
    def text(self) -> str:
        """Textuelle Darstellung des gesprochenen Inhalts

        :return: Text
        :rtype: str
        """
        return " ".join(self.words)
    
    @property
    def word_count(self) -> int:
        """Anzahl der Wörter des gesprochenen Inhalts

        :return: Anzahl Wörter
        :rtype: int
        """
        return len(self.words)
    
    def has_words(self, words: List[str]) -> List[WordPresent]:
        """Prüft ob die Wübergebenen Wörter im gesprochenen Inhalt enthalten sind

        :param words: Liste mit Wörtern die geprüft werden soll
        :type words: List[str]
        :return: List mit  Ergebnissen zu jedem Wort das überprüft werden sollte
        :rtype: List[WordPresent]
        """
        return [WordPresent(word=word, present=word in self.words) for word in [w.lower() for w in words]]

    def _bytes_to_mono_wav(self, stereo_wav: bytes) -> Wave_read:
        """Konvertiert Stero WAV Daten in Mono WAV Daten

        :param stereo_wav: Daten einer WAV Datei (Stereo oder Mono)
        :type stereo_wav: bytes
        :return: Daten als Mono WAV
        :rtype: Wave_read
        """
        _time_sart: datetime = datetime.now()
        out_buffer = io.BytesIO()
        wav = wave.open(io.BytesIO(stereo_wav),'rb')
        if wav.getnchannels() > 1:
            out_wav = wave.open(out_buffer,'wb')
            out_wav.setnchannels(1)
            out_wav.setsampwidth(wav.getsampwidth())
            out_wav.setframerate(wav.getframerate())
            out_wav.writeframes(audioop.tomono(wav.readframes(wav.getnframes()), wav.getsampwidth(), 1, 1))
            out_wav.close()
            out_buffer.seek(0)
            wav = wave.open(out_buffer,'rb')
        self.time_convert: timedelta = datetime.now() - _time_sart
        return wav
    
    def _mp3_to_wav(self, mp3: bytes) -> bytes:
        """Konvertiert MP3-Daten zu WAV-Daten (Stereo)

        :param mp3: _description_
        :type mp3: bytes
        :return: _description_
        :rtype: bytes
        """
        buffer = io.BytesIO(mp3)
        buffer.seek(0)
        sound = AudioSegment.from_mp3(buffer)
        out_buffer = io.BytesIO()
        sound.export(out_buffer, format="wav")
        out_buffer.seek(0)
        return out_buffer.read()

    def _analyze_text(self):
        """Startet die analyse der Mono WAV Daten
        """
        _time_sart: datetime = datetime.now()
        recognizer = KaldiRecognizer(self.__SPEECH_MODEL, self.wave.getframerate())
        recognizer.SetWords(True)
        while len(data := self.wave.readframes(4000)) != 0:
            if recognizer.AcceptWaveform(data):
                if tmp_result := json.loads(recognizer.Result()).get('result'):
                    self.analyze_result += tmp_result
        if tmp_result := json.loads(recognizer.FinalResult()).get('result'):
            self.analyze_result += tmp_result
        self._clean_results()
        self.time_analyze: timedelta = datetime.now() - _time_sart

    def _analyze_grammar(self):
        """Analysiert die Grammatik des gesprochenen Inhalts
        """
        errors: List[Match] = self.__GRAMMAR_TOOL.check(self.text)
        self.grammar: List[GrammarError] = []
        for error in errors:
            if error.category == 'GRAMMAR':
                self.grammar.append(
                    GrammarError(
                        message = error.message,
                        offset = error.offset,
                        length = error.errorLength,
                        suggestion = error.replacements[0] if len(error.replacements) > 0 else ''
                    )
                )

    def _analyze_meta(self) -> None:
        """Startet die Analyse der Metadaten der Audio Daten
        """
        self.duration: float = self.wave.getnframes()/float(self.wave.getframerate())

    def _clean_results(self) -> None:
        """Setzt die Ergebnisse zurück (Noch nicht vollständig implementiert)
        """
        for index, result in enumerate(self.analyze_result):
            if index == 0:
                ...#result['word'] = result['word'].capitalize()
            if result['word'] == 'ah':
                result['word'] = 'a'