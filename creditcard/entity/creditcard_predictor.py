import os
import sys

from creditcard.exception import CreditcardException
from creditcard.util.util import load_object

import pandas as pd


class CreditcardData:

    def __init__(self,
                 ID: float,
                 LIMIT_BAL: float,
                 SEX: float,
                 EDUCATION: float,
                 MARRIAGE: float,
                 AGE: float,
                 PAY_0: float,
                 PAY_2: float,
                 PAY_3: float,
                 PAY_4: float,
                 PAY_5: float,
                 PAY_6: float,
                 BILL_AMT1: float,
                 BILL_AMT2: float,
                 BILL_AMT3: float,
                 BILL_AMT4: float,
                 BILL_AMT5: float,
                 BILL_AMT6: float,
                 PAY_AMT1: float,
                 PAY_AMT2: float,
                 PAY_AMT3: float,
                 PAY_AMT4: float,
                 PAY_AMT5: float,
                 PAY_AMT6: float,
                 default_payment_next_month: float=None
                 ):
        try:
            self.ID = ID
            self.LIMIT_BAL = LIMIT_BAL
            self.SEX = SEX
            self.EDUCATION = EDUCATION
            self.MARRIAGE = MARRIAGE
            self.AGE = AGE
            self.PAY_0 = PAY_0
            self.PAY_2 = PAY_2
            self.PAY_3 = PAY_3
            self.PAY_4 = PAY_4
            self.PAY_5 = PAY_5
            self.PAY_6 = PAY_6
            self.BILL_AMT1 = BILL_AMT1
            self.BILL_AMT2 = BILL_AMT2
            self.BILL_AMT3 = BILL_AMT3
            self.BILL_AMT4 = BILL_AMT4
            self.BILL_AMT5 = BILL_AMT5
            self.BILL_AMT6 = BILL_AMT6
            self.PAY_AMT1 = PAY_AMT1
            self.PAY_AMT2 = PAY_AMT2
            self.PAY_AMT3 = PAY_AMT3
            self.PAY_AMT4 = PAY_AMT4
            self.PAY_AMT5 = PAY_AMT5
            self.PAY_AMT6 = PAY_AMT6
            self.default_payment_next_month = default_payment_next_month
        except Exception as e:
            raise CreditcardException(e, sys) from e

    def get_creditcard_input_data_frame(self):

        try:
            creditcard_input_dict = self.get_creditcard_data_as_dict()
            return pd.DataFrame(creditcard_input_dict)
        except Exception as e:
            raise CreditcardException(e, sys) from e

    def get_creditcard_data_as_dict(self):
        try:
            input_data =   {"ID": [self.ID],
                            "LIMIT_BAL": [self.LIMIT_BAL],
                            "SEX": [self.SEX],
                            "EDUCATION": [self.EDUCATION],
                            "MARRIAGE": [self.MARRIAGE],
                            "AGE": [self.AGE],
                            "PAY_0": [self.PAY_0],
                            "PAY_2": [self.PAY_2],
                            "PAY_3": [self.PAY_3],
                            "PAY_4": [self.PAY_4],
                            "PAY_5": [self.PAY_5],
                            "PAY_6": [self.PAY_6],
                            "BILL_AMT1": [self.BILL_AMT1],
                            "BILL_AMT2": [self.BILL_AMT2],
                            "BILL_AMT3": [self.BILL_AMT3],
                            "BILL_AMT4": [self.BILL_AMT4],
                            "BILL_AMT5": [self.BILL_AMT5],
                            "BILL_AMT6": [self.BILL_AMT6],
                            "PAY_AMT1": [self.PAY_AMT1],
                            "PAY_AMT2": [self.PAY_AMT2],
                            "PAY_AMT3": [self.PAY_AMT3],
                            "PAY_AMT4": [self.PAY_AMT4],
                            "PAY_AMT5": [self.PAY_AMT5],
                            "PAY_AMT6": [self.PAY_AMT6]}
            return input_data
        except Exception as e:
            raise CreditcardException(e, sys)


class CreditcardPredictor:
    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise CreditcardException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(str, os.listdir(self.model_dir)))
            latest_model_path = os.path.join(self.model_dir, f"{max(folder_name)}")
            #file_name = os.listdir(latest_model_dir)[0]
            #latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise CreditcardException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            default_payment_next_month = model.predict(X)
            return default_payment_next_month
        except Exception as e:
            raise CreditcardException(e, sys) from e