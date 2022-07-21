from evidently import dashboard
from matplotlib.pyplot import flag
from creditcard.logger import logging
from creditcard.exception import CreditcardException
from creditcard.config.configuration import Configuration
from creditcard.entity.config_entity import DataValidationConfig
from creditcard.entity.artifact_config import DataIngestionArtifact,DataValidationArtifact
import sys
import os
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json
from creditcard.util.util import read_yaml_file
from creditcard.contants import SCHEMA_CONFIG_FILE_PATH



class DataValidation():
    def __init__(self,data_validation_config:DataValidationConfig,
        data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data validation log started {'<<'*30}")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
        except Exception as e:
            raise CreditcardException(e,sys) from e
    #------------------------------------------
    def is_train_test_file_exists(self)->bool:
        try:
            logging.info(f"Checking whether train and test files exist or not")
            is_train_file_exists = False
            is_test_file_exists = False
            
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exists = os.path.exists(train_file_path)
            is_test_file_exists = os.path.exists(test_file_path)
            is_train_test_file_exists = is_train_file_exists and is_test_file_exists
            logging.info(f"Is train and test file exists?-> {is_train_test_file_exists}")

            if not is_train_test_file_exists:
                logging.info(f"Training file or testing file not present")
            
            return is_train_test_file_exists
        except Exception as e:
            raise CreditcardException(e,sys) from e
    #-----------------------------------------------
    def get_schema_structure(self):
        try:
            schema_file = read_yaml_file(file_path=SCHEMA_CONFIG_FILE_PATH)
            return schema_file
        except Exception as e:
            raise CreditcardException(e,sys) from e
    #-----------------------------------------------
    def verify_column_count(self)->bool:
        try:
            is_column_count_correct = False
            schema_file = self.get_schema_structure()
            train_df,test_df = self.get_train_and_test_df()

            schema_col_count = len(list(schema_file['columns'].keys()))
            train_col_count = len(list(train_df.columns))
            test_col_count = len(list(test_df.columns))
            is_column_count_correct = (schema_col_count == train_col_count)and(schema_col_count == test_col_count)
            return is_column_count_correct

        except Exception as e:
            raise CreditcardException(e,sys) from e
    #-----------------------------------------------
    def check(self,col)->bool:
        try:
            flag = False
            schema_cols = ['ID', 'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE', 
                           'PAY_0','PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'BILL_AMT1',
                           'BILL_AMT2','BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
                           'PAY_AMT1','PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5',
                           'PAY_AMT6','default.payment.next.month']
            flag = col in schema_cols
            return flag
        except Exception as e:
            raise CreditcardException(e,sys) from e

    #-----------------------------------------------
    def verify_column_names(self):
        try:
            is_column_names_correct = False
            train_df,test_df = self.get_train_and_test_df()
            train_flags = list(map(self.check,list(train_df.columns)))
            test_flags  = list(map(self.check,list(test_df.columns)))

            train_flag = set(train_flags)
            test_flag  = set(test_flags)
            
            i=0
            for j in train_flags:
                if (train_flags[i]==False):
                    logging.info(f"Training column no:[{i}] is mismatching with schema file")
                i=i+1
            l=0
            for k in test_flags:
                if (test_flags[l]==False):
                    logging.info(f"Testing column no:[{l}] is mismatching with schema file")
                l=l+1
            train_flag = not(False in train_flag)
            test_flag  = not(False in test_flag)

            is_column_names_correct = train_flag and test_flag
            return is_column_names_correct

        except Exception as e:
            raise CreditcardException(e,sys) from e
    #-----------------------------------------------
    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False
            is_column_count_correct = self.verify_column_count()
            is_column_names_correct = self.verify_column_names()
            validation_status = is_column_count_correct and is_column_names_correct
            return validation_status

        except Exception as e:
            raise CreditcardException(e,sys) from e
    #-----------------------------------------------
    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise CreditcardException(e,sys) from e
    #-----------------------------------------------
    def save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df,test_df = self.get_train_and_test_df()
            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path, "w") as report_file:
                json.dump(report,report_file,indent=4)
            return report
        except Exception as e:
            raise CreditcardException(e,sys) from e
    #------------------------------------------------
    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir,exist_ok=True)

            dashboard.save(report_page_file_path)

        except Exception as e:
            raise CreditcardException(e,sys) from e
    #-------------------------------------------------
    def is_data_drift_found(self)->bool:
        try:
            self.save_data_drift_report()
            self.save_data_drift_report_page()

            report_file_path = self.data_validation_config.report_file_path

            with open(report_file_path,'r') as json_file:
                report_dict = json.load(json_file)
            is_data_drift_found = report_dict['data_drift']['data']['metrics']['dataset_drift']

            if not is_data_drift_found:
                train_file_path = self.data_ingestion_artifact.train_file_path
                test_file_path = self.data_ingestion_artifact.test_file_path
                logging.info(f"Datadrift not found for [{train_file_path}] and [{test_file_path}]")
            logging.info(f"{'<<'*15} Data validation log completed {'<<'*15}")

            return is_data_drift_found
        except Exception as e:
            raise CreditcardException(e,sys) from e
    

    #----------------------All in one function--------------------------#
    def initiate_data_validation_stage(self)->DataValidationArtifact:
        try:
            logging.info(f"{'<<'*15} Data validation log started {'<<'*15}")
            self.is_train_test_file_exists()
            validation_status = self.validate_dataset_schema()
            if (validation_status == True):
                is_data_drift_found = self.is_data_drift_found()
                logging.info(f"Is Data drift found? [{is_data_drift_found}]")

            data_validation_artifact = DataValidationArtifact(
                schema_file_path = self.data_validation_config.schema_file_path,
                report_file_path = self.data_validation_config.report_file_path,
                report_page_file_path = self.data_validation_config.report_page_file_path,
                is_validated = validation_status,
                message = f"Data Validation performed successfully"
            )
            return data_validation_artifact
        except Exception as e:
            raise CreditcardException(e,sys) from e