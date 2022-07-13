from logging import exception
from flask import Flask,request
from creditcard.logger import logging
from creditcard.exception import CreditcardException
import sys


app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    try:
        raise Exception("we raised exception")
    except Exception as e:
        creditobj = CreditcardException(e,sys)
        logging.info(creditobj.error_message)
        return "Exception is fine"

if __name__== "__main__":
    app.run()