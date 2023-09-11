from typing import *
import pandas as pd
import numpy as np
from io import BytesIO
from db import db
from log import logging as log
WORDS_FILE_FOLDER: str = './words'

class Words:
    """Wortdatenbank Objekt (liefert grundlegende Funktionalitäten um auf die Wortdatenbank zuzugreifen)

    :raises Exception: Ausnahme wenn keine Wortdatenbank angelegt wurde
    """
    __dbRecName: str = 'WordDataSUB.linqua'
    def __init__(self) -> None:
        """Konstruktor eines Wortdatenbank Objekts

        :raises Exception: _description_
        """
        log.info('loading word data')
        pickled_word_data: bytes = db.files.find_one({'filename': self.__dbRecName})
        if not pickled_word_data:
            log.error(errmsg := 'no word data in DB')
            raise Exception(errmsg)
        self.__words: pd.DataFrame = pd.read_pickle(pickled_word_data)
    
    @property
    def classes(self) -> List[str]:
        """Liefert alle verfügbaren Wortklassen

        :return: Liste der Wortklassen
        :rtype: List[str]
        """
        word_types = [t for t in self.__words['Type'].unique()]
        word_types.sort()
        return word_types
    
    @property
    def overview(self) -> Dict:
        """Übersicht der Wortdatenbank

        :return: Informationen zur Wortdatenban
        :rtype: Dict
        """
        return dict(
            word_count = len(self.__words),
            classes = self.classes
        )

    @staticmethod
    def update(words_data: bytes) -> bool:
        """Updatet den Inhalt der Wortdatenbank (durch SUBTLEX .xlsx Datei)

        :param words_data: Wortdaten Datei
        :type words_data: bytes
        :return: Erfolgreich (Ja/Nein)
        :rtype: bool
        """     
        try:
            dfwords = Words.__clean_subtlex_data(pd.read_excel(words_data))
            buffer = BytesIO()
            dfwords.to_pickle(buffer)
            buffer.seek(0)
            for old_file_id in db.files.find({'filename': Words.__dbRecName}).distinct('_id'):
                db.files.delete(old_file_id)
                log.info(f'removed existing word data - {old_file_id}')
            db.files.put(buffer.read(), filename=Words.__dbRecName)
            log.info('word db updated')
            return True
        except Exception as e:
            log.error('error updating word database')
            log.debug(e)
        return False

    @staticmethod
    def __clean_subtlex_data(df: pd.DataFrame) -> pd.DataFrame:
        """Grundlegende Aufbereitung der Wortdaten aus SUBTLEX Datei

        :param df: Wortdaten
        :type df: pd.DataFrame
        :return: Bereinigte Wortdaten
        :rtype: pd.DataFrame
        """
        # remove unimportant wort types
        df = df[(~df['Dom_PoS_SUBTLEX'].isin(['Letter', 'Unclassified', 'To', 'Not', 'Ex', np.nan]))]
        
        # remove words with unclear wordtype
        df = df[(df['Percentage_dom_PoS'] > 0.9)]
       
        # normalize SUBTLCD
        df['SUBTLCD'] = df['SUBTLCD']/100
       
        # rename columns
        df = df[['Word', 'SUBTLCD', 'Dom_PoS_SUBTLEX']].rename(columns={'SUBTLCD':'Frequency', 'Dom_PoS_SUBTLEX':'Type'})
        
        # calculate frequenzy range of availbe word types
        def calc_min_max(s):
            type_seq = df[(df['Type'] == s['Type'])]['Frequency']
            s['Min'] = type_seq.min()
            s['Max'] = type_seq.max()
            return s
        word_types_frequency_range = pd.DataFrame({'Type': df['Type'].unique()}).apply(calc_min_max, axis=1)
        
        # calculate normalized frequenzy by type
        def calculate_typed_frequency(s):
            wtfr = word_types_frequency_range[(word_types_frequency_range['Type'] == s['Type'])]
            return ((s['Frequency'] - wtfr['Min'].iloc[0])/(wtfr['Max'].iloc[0] - wtfr['Min'].iloc[0]))

        df['FrequencyType'] = df.apply(lambda x: calculate_typed_frequency(x), axis=1)

        # reset index
        df.reset_index(drop=True, inplace=True)
        return df
    
    def get(self, word_type: str, amount: int, min_freq: float = 0.0, max_freq: float = 1.0) -> List[str]:
        """Liefert zufällige Wörter mit den vorgegeben Bedingungen

        :param word_type: Wortklasse
        :type word_type: str
        :param amount: Anzahl der Wörter
        :type amount: int
        :param min_freq: niedrigste Frequenz der Wörter (schwierigkeit obere schranke), defaults to 0.0
        :type min_freq: float, optional
        :param max_freq: höchste Frequentz der Wörter (schwierigkeit untere Schranke), defaults to 1.0
        :type max_freq: float, optional
        :return: Liste mit Wörtern
        :rtype: List[str]
        """
        available_words = self.__words[(self.__words['Type'] == word_type) & (self.__words['FrequencyType'] >= min_freq) & (self.__words['FrequencyType'] <= max_freq)]['Word']
        return [word for word in available_words.sample(amount if len(available_words) >= amount else len(available_words))]
