from tkinter.messagebox import NO
from creditcard.logger import logging
from creditcard.exception import CreditcardException
from creditcard.entity.config_entity import DataIngestionConfig
from creditcard.entity.artifact_config import DataIngestionArtifact
import os
from six.moves import urllib
from  zipfile import ZipFile
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion():
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise CreditcardException(e,sys) from e
    def download_credicard_dataset(self)->str:
        try:
            #getting download url from dataingestion config object
            download_url=self.data_ingestion_config.dataset_download_url

            #folder location to store downloaded dataset
            zip_data_dir=self.data_ingestion_config.zip_data_dir

            os.makedirs(zip_data_dir,exist_ok=True)

            creditcard_filename = os.path.basename(download_url)

            zip_file_path=os.path.join(zip_data_dir,creditcard_filename)
            logging.info(f"Downloading file from:[{download_url}] into [{zip_file_path}]")

            urllib.request.urlretrieve(download_url,zip_file_path)
            logging.info(f"File[{creditcard_filename}] has been downloaded to:[{zip_file_path}]")

            return zip_file_path
        except Exception as e:
            raise CreditcardException(e,sys) from e

    def extract_zip_file(self,zip_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting :[{zip_file_path}] into dir:[{raw_data_dir}]")
            with ZipFile(zip_file_path,'r') as creditcard_zipfile_obj:
                creditcard_zipfile_obj.extractall(raw_data_dir)
            logging.info(f"Extraction completed")

        except Exception as e:
            raise CreditcardException(e,sys) from e

    def split_dataset_as_train_test(self)->DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            creditcard_dataset_filepath = os.path.join(raw_data_dir,
            file_name
            )

            logging.info(f"Reading csv file:{creditcard_dataset_filepath}")
            creditcard_dataframe = pd.read_csv(creditcard_dataset_filepath)
            logging.info(f"Splitting dataset into train and test")

            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=10)

            for train_ix,test_ix in split.split(creditcard_dataframe,creditcard_dataframe['default.payment.next.month']):
                strat_train_set = creditcard_dataframe.loc[train_ix]
                strat_test_set = creditcard_dataframe.loc[test_ix]
            
            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
            file_name
            )
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
            file_name
            )

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting Training dataset to:[{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)
            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                logging.info(f"Exporting Testing dataset to:[{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            
            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
            test_file_path=test_file_path,
            is_ingested=True,
            message=f"Data ingestion completed successfully."
            )

        except Exception as e:
            raise CreditcardException(e,sys) from e

    #All above functions included in below function
    def initiate_dataingestion_stage(self)->DataIngestionArtifact:
        try:
            zip_file_path = self.download_credicard_dataset()
            self.extract_zip_file(zip_file_path=zip_file_path)
            return self.split_dataset_as_train_test()
        except Exception as e:
            raise CreditcardException(e,sys) from e