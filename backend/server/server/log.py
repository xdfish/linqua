import logging, pathlib

pathlib.Path('./log').mkdir(exist_ok=True)

logging.basicConfig(
    filename='log/linqua.log',
    filemode='a',
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    level=logging.DEBUG
    )



