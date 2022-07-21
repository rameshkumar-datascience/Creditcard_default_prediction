import sys
from creditcard.logger import logging
from creditcard.exception import CreditcardException
from creditcard.config.configuration import Configuration
from creditcard.stages.data_ingestion import DataIngestion
from creditcard.stages.data_validation import DataValidation
from creditcard.stages.data_transformation import DataTransformation
from creditcard.entity.config_entity import DataIngestionConfig, DataValidationConfig,DataTransformationConfig
from creditcard.entity.artifact_config import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact





class Pipeline():
    def __init__(self,config:Configuration) -> None:
        try:
            self.config=config
        except Exception as e:
            raise CreditcardException(e,sys) from e
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(self.config.get_data_ingestion_pipeline_config())
            return data_ingestion.initiate_dataingestion_stage()
        except Exception as e:
            raise CreditcardException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_validation = DataValidation(self.config.get_data_validation_config(),
            data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation_stage()
        except Exception as e:
            raise CreditcardException(e,sys) from e
    
    def start_data_transformation(self,
                                  data_ingestion_artifact:DataIngestionArtifact,
                                  data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(data_transformation_config=self.config.get_data_transformation_config(),
                                                     data_ingestion_artifact=data_ingestion_artifact,
                                                     data_validation_artifact=data_validation_artifact
                                                     )
            return data_transformation.initiate_data_transformation_stage()
    
        except Exception as e:
            raise CreditcardException(e,sys)

    def start_model_trainer(self,)->ModelTrainerArtifact:
        try:
            pass
        except Exception as e:
            raise CreditcardException(e,sys) from e


    #----------------------All in one function--------------------------#
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                        data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            #model_evaluation_artifact = self.start_model_evaluation(model_trainer_artifact=model_trainer_artifact)
            #model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)

        except Exception as e:
            raise CreditcardException(e,sys) from e