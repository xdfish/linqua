from typing import *
from vosk import Model, KaldiRecognizer, SetLogLevel
import wave, io, json, audioop
from datetime import datetime, timedelta
from wave import Wave_read
from pydub import AudioSegment

SetLogLevel(-1)
MODEL = [
    'model/vosk-model-en-us-0.22',
    'model/vosk-model-en-us-0.42-gigaspeech',
    'model/vosk-model-en-us-daanzu-20200905', #Fastest Model, no error words for now
    'model/vosk-model-en-us-daanzu-20200905-lgraph'
]

class Speech:    
    model = Model(MODEL[1])
    time_convert: timedelta
    time_analyze: timedelta
    def __init__(self, audio: bytes, audio_type: str = 'wav') -> None:
        self.analyze_result: List[Dict] = []
        self.audio: bytes = audio
        if audio_type == 'mp3':
            audio = self._mp3_to_wav(audio)
        self.wave: Wave_read = self._bytes_to_mono_wav(audio)
        self._analyze_text()
    
    @property
    def words(self) -> List[str]:
        return [result['word'] for result in self.analyze_result]
    
    @property
    def text(self) -> str:
        return " ".join(self.words)
    
    @property
    def word_count(self) -> int:
        return len(self.words)
    
    def has_words(self, words: List[str]) -> Dict[str, bool]:
        return {word : word in self.words for word in [w.lower() for w in words]}

    def _bytes_to_mono_wav(self, stereo_wav: bytes) -> Wave_read:
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
        buffer = io.BytesIO(mp3)
        buffer.seek(0)
        sound = AudioSegment.from_mp3(buffer)
        out_buffer = io.BytesIO()
        sound.export(out_buffer, format="wav")
        out_buffer.seek(0)
        return out_buffer.read()

    def _analyze_text(self):
        _time_sart: datetime = datetime.now()
        recognizer = KaldiRecognizer(self.model, self.wave.getframerate())
        recognizer.SetWords(True)
        while len(data := self.wave.readframes(4000)) != 0:
            if recognizer.AcceptWaveform(data):
                self.analyze_result += json.loads(recognizer.Result())['result']
        self.analyze_result += json.loads(recognizer.FinalResult())['result']
        self._clean_results()
        self.time_analyze: timedelta = datetime.now() - _time_sart

    def _clean_results(self):
        for index, result in enumerate(self.analyze_result):
            if index == 0:
                ...#result['word'] = result['word'].capitalize()
            if result['word'] == 'ah':
                result['word'] = 'a'