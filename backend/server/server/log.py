import logging, pathlib

#Erzeugen des log ordners (wenn er nicht existiert)
pathlib.Path('./log').mkdir(exist_ok=True)

#Anpassen des logging Formats und umleiten der logs in die datei log/linqua.log
logging.basicConfig(
    filename='log/linqua.log',
    filemode='a',
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    level=logging.DEBUG
    )



