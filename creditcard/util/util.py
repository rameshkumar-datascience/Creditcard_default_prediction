import yaml
from creditcard.contants import *
from creditcard.logger import logging
from creditcard.exception import CreditcardException

def read_yaml_file(file_path:str)->dict:
    """
    This function will take filepath as argument
    and returns config.yaml file as a dictionary
    """
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CreditcardException(e,sys) from e