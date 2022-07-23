import sys
from creditcard.logger import logging
from creditcard.exception import CreditcardException
from creditcard.config.configuration import Configuration
from creditcard.stages.data_ingestion import DataIngestion
from creditcard.stages.data_validation import DataValidation
from creditcard.stages.data_transformation import DataTransformation
from creditcard.stages.model_trainer import ModelTrainer
from creditcard.stages.model_evaluation import ModelEvaluation
from creditcard.stages.model_pusher import ModelPusher
from creditcard.entity.config_entity import DataIngestionConfig, DataValidationConfig,DataTransformationConfig
from creditcard.entity.artifact_config import DataIngestionArtifact,DataValidationArtifact, \
DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact





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

    def start_model_trainer(self,
                            data_transformation_artifact:DataTransformationArtifact,
                            )->ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                         data_transformation_artifact=data_transformation_artifact
                                         )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise CreditcardException(e,sys) from e

    def start_model_evaluation(self, data_ingestion_artifact: DataIngestionArtifact,
                               data_validation_artifact: DataValidationArtifact,
                               model_trainer_artifact: ModelTrainerArtifact)->ModelEvaluationArtifact:
        try:
            model_eval = ModelEvaluation(
                model_evaluation_config=self.config.get_model_evaluation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact,
                model_trainer_artifact=model_trainer_artifact)
            return model_eval.initiate_model_evaluation()
        except Exception as e:
            raise CreditcardException(e, sys) from e

    def start_model_pusher(self, model_eval_artifact: ModelEvaluationArtifact)->ModelPusherArtifact:
        try:
            model_pusher = ModelPusher(
                model_pusher_config=self.config.get_model_pusher_config(),
                model_evaluation_artifact=model_eval_artifact
            )
            return model_pusher.initiate_model_pusher()
            
        except Exception as e:
            raise CreditcardException(e, sys) from e


    #----------------------All in one function--------------------------#
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                        data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            
            model_evaluation_artifact = self.start_model_evaluation(data_ingestion_artifact=data_ingestion_artifact,
                                                                    data_validation_artifact=data_validation_artifact,
                                                                    model_trainer_artifact=model_trainer_artifact)
        
            
            if model_evaluation_artifact.is_model_accepted:
                model_pusher_artifact = self.start_model_pusher(model_eval_artifact=model_evaluation_artifact)
                logging.info(f'Model pusher artifact: {model_pusher_artifact}')
            else:
                logging.info("Trained model rejected.")
        
        except Exception as e:
            raise CreditcardException(e,sys) from e