import sys
from creditcard.logger import logging
from creditcard.exception import CreditcardException
from creditcard.config.configuration import Configuration
from creditcard.stages.data_ingestion import DataIngestion
from creditcard.entity.config_entity import DataIngestionConfig
from creditcard.entity.artifact_config import DataIngestionArtifact





class Pipeline():
    def __init__(self,config:Configuration) -> None:
        try:
            self.config=config
        except Exception as e:
            raise CreditcardException(e,sys) from e
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion_config = DataIngestion(self.config.get_data_ingestion_pipeline_config())
            return data_ingestion_config.initiate_dataingestion_stage()
        except Exception as e:
            raise CreditcardException(e,sys)