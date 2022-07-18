from logging import raiseExceptions
from tkinter import E
from creditcard.logger import logging
from creditcard.exception import CreditcardException
from creditcard.contants import *
from creditcard.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from creditcard.util.util import read_yaml_file
import os
import sys
class Configuration():
    def __init__(self,
        config_file_path:str=CONFIG_FILE_PATH,
        current_time_stamp:str=CURRENT_TIMESTAMP
        )->None:
        try:
            self.config_info = read_yaml_file(file_path=config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.current_time_stamp = current_time_stamp
        except Exception as e:
            raise CreditcardException(e,sys) from e

    #Defing pipelinename and artifact folder names for entire project 
    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_ARTIFIFACT_DIR_NAME_KEY]
            )

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training Pipeline config:{training_pipeline_config}")

            return training_pipeline_config
        except Exception as e:
            raise CreditcardException(e,sys) from e
    
    #defining configuration for dataingestion
    def get_data_ingestion_pipeline_config(self)->DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(artifact_dir,
            DATA_INGESTION_ARTIFACT_DIR,
            self.current_time_stamp
            )

            data_ingestion_config_info = self.config_info[DATA_INGESTION_CONFIG_KEY]
            download_url = data_ingestion_config_info[DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY]
            
            zip_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_ZIP_DATA_DIR_KEY]
            )

            raw_data_dir= os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_RAW_DATA_DIR_KEY]
            )

            ingested_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_config_info[DATA_INGESTION_INGESTED_DIR_KEY]
            )

            train = os.path.join(ingested_dir,
            data_ingestion_config_info[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY]
            )

            test = os.path.join(ingested_dir,
            data_ingestion_config_info[DATA_INGESTION_INGESTED_TEST_DIR_KEY]
            )

            data_ingestion_config = DataIngestionConfig(dataset_download_url=download_url,
            zip_data_dir=zip_data_dir,
            raw_data_dir=raw_data_dir,
            ingested_dir=ingested_dir,
            ingested_train_dir=train,
            ingested_test_dir=test
            )

            logging.info(f"DataIngestionConfig:{data_ingestion_config}")

            return data_ingestion_config

        except Exception as e:
            raise CreditcardException(e,sys) from e
    
    def get_data_validation_config(self):
        try:
            pass
        except Exception as e:
            raise CreditcardException(e,sys) from e
    
    def get_data_transformation_config():
        try:
            pass
        except Exception as e:
            raise CreditcardException(e,sys) from e
    def get_model_trainer_config():
        try:
            pass
        except Exception as e:
            raise CreditcardException(e,sys) from e
    def get_model_evaluation_config():
        try:
            pass
        except Exception as e:
            raise CreditcardException(e,sys) from e
    def get_model_pusher_config():
        try:
            pass
        except Exception as e:
            raise CreditcardException(e,sys) from e

