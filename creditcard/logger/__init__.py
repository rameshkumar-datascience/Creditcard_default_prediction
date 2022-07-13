import logging
from creditcard.contants import CURRENT_TIMESTAMP
import os


LOG_DIR="logs"
os.makedirs(LOG_DIR,exist_ok=True)
LOG_FILENAME=f"log_{CURRENT_TIMESTAMP}.log"
LOG_FILEPATH=os.path.join(LOG_DIR,LOG_FILENAME)

logging.basicConfig(
    filename=LOG_FILEPATH,
    filemode='w',
    format='[%(asctime)s]^;%(levelname)s^;%(lineno)d^;%(filename)s^;%(funcName)s()^;%(message)s',
    level=logging.INFO
)