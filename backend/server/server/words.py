import pandas as pd
import numpy as np
from io import BytesIO
from db import db
from log import logging as log
WORDS_FILE_FOLDER: str = './words'

class Words:
    __dbRecName: str = 'WordDataSUB.linqua'
    def __init__(self) -> None:
        log.info('loading word data')
        pickled_word_data: bytes = db.files.find_one({'filename': self.__dbRecName})
        if not pickled_word_data:
            log.error(errmsg := 'no word data in DB')
            raise Exception(errmsg)
        self.__words: pd.DataFrame = pd.read_pickle(pickled_word_data)
    
    @staticmethod
    def update(words_data: bytes):
        dfwords = Words.__clean_subtlex_data(pd.read_excel(words_data))
        buffer = BytesIO()
        dfwords.to_pickle(buffer)
        buffer.seek(0)
        db.files.put(buffer.read(), filename=Words.__dbRecName)

    @staticmethod
    def __clean_subtlex_data(df: pd.DataFrame) -> pd.DataFrame:
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
    
    def get(self, word_type: str, amount: int, min_freq: float = 0.0, max_freq: float = 1.0):
        available_words = self.__words[(self.__words['Type'] == word_type) & (self.__words['FrequencyType'] >= min_freq) & (self.__words['FrequencyType'] <= max_freq)]['Word']
        return [word for word in available_words.sample(amount if len(available_words) >= amount else len(available_words))]

    @property
    def classes(self):
        word_types = [t for t in self.__words['Type'].unique()]
        word_types.sort()
        return word_types