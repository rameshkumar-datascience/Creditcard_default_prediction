from datetime import datetime
import os

def get_current_timestamp():
    return f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}"

ROOT_DIR=os.getcwd()
CURRENT_TIMESTAMP=get_current_timestamp()