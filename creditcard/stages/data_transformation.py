from shutil import ExecError
import sys
from sklearn import preprocessing
from creditcard.logger import logging
from creditcard.exception import CreditcardException
from creditcard.entity.config_entity import DataTransformationConfig
from creditcard.entity.artifact_config import DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from creditcard.util.util import read_yaml_file,save_numpy_array_data, save_object
from creditcard.contants import *
import pandas as pd
import numpy as np



class DataTransformation:
    def __init__(self, data_transformation_config:DataTransformationConfig,
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_artifact:DataValidationArtifact):
        try:
            logging.info(f"{'<<'*15} Data Transformation log started {'>>'*15}")
            self.data_transformation_config = data_transformation_config
            logging.info(f"Datatransformationconfig:{self.data_transformation_config}")
            print(self.data_transformation_config)
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise CreditcardException(e,sys)
    
    def get_data_transformer_object(self)->ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifact.schema_file_path
            dataset_schema = read_yaml_file(file_path=schema_file_path)

            numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]
            num_pipeline = Pipeline(steps=[
                ('impute',SimpleImputer(strategy='mean')),
                ('scaler',StandardScaler())])
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessed_obj=ColumnTransformer([('num_pipeline',num_pipeline,numerical_columns)])

            return preprocessed_obj

        except Exception as e:
            raise CreditcardException(e,sys) from e

    def datatypes_correction(self,file_Path:str, schema_file_path:str):
        try:
            dataset_schema = read_yaml_file(file_path=schema_file_path)
            schema = dataset_schema[SCHEMA_COLUMN_KEY]

            dataframe = pd.read_csv(file_Path)
            error_message = ""

            for column in dataframe.columns:
                if column in list(schema.keys()):
                    dataframe[column].astype(schema[column])
            else:
                error_message = f"{error_message} \nColumn: [{column}] is not in the schema." 
            
            return dataframe
        except Exception as e:
            raise CreditcardException(e,sys) from e
    
    def get_and_save_numpy_array_data(self,train_df,
                                      test_df,
                                      schema,
                                      preprocessed_obj):
        try:

            target_column_name = schema[TARGET_COLUMN_KEY]
            logging.info(f"Splitting input and target feature from training and testing dataframe.")
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
            input_feature_train_arr = preprocessed_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessed_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[ input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            train_file_path = self.data_ingestion_artifact.train_file_path 
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_file_name = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_name = os.path.basename(test_file_path).replace(".csv",".npz")
             
            transformed_train_dir = self.data_transformation_config.transformed_train_dir
            transformed_test_dir = self.data_transformation_config.transformed_test_dir

            transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
            transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

            logging.info(f"Saving transformed training and testing array.")

            save_numpy_array_data(file_path=transformed_train_file_path,array=train_arr)
            save_numpy_array_data(file_path=transformed_test_file_path,array=test_arr)
            
            #We are returning paths because we need this to preparation of artifact info
            return transformed_train_file_path,transformed_test_file_path
        except Exception as e:
            raise CreditcardException(e,sys) from e

    #-----------------All in one function------------------------#
    def initiate_data_transformation_stage(self)->DataTransformationArtifact:
        try:
            preprocessed_obj=self.get_data_transformer_object()

            logging.info(f"Obtaining training and test file path.")
            train_file_path = self.data_ingestion_artifact.train_file_path 
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path
            schema = read_yaml_file(file_path=schema_file_path)
            train_df = self.datatypes_correction(file_Path=train_file_path,schema_file_path=schema_file_path)
            test_df = self.datatypes_correction(file_Path=test_file_path,schema_file_path=schema_file_path)

            transformed_train_file_path,transformed_test_file_path = self.get_and_save_numpy_array_data(train_df=train_df,
                                                                                                        test_df=test_df,
                                                                                                        schema=schema,
                                                                                                        preprocessed_obj=preprocessed_obj)
            
            preprocessed_obj_file_path = self.data_transformation_config.preprocessed_object_file_path
            logging.info(f"Saving preprocessing object.")
            save_object(file_path=preprocessed_obj_file_path,obj=preprocessed_obj)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
            message="Data transformation successfull.",
            transformed_train_file_path =transformed_train_file_path,
            transformed_test_file_path=transformed_test_file_path,
            preprocessed_object_file_path=preprocessed_obj_file_path
            )

            logging.info(f"Data transformationa artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise CreditcardException(e,sys)