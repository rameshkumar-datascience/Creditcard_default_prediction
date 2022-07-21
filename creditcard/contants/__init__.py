from datetime import datetime
import os

def get_current_timestamp():
    return f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}"

ROOT_DIR=os.getcwd()
CONFIG_DIR="config_info"
CONFIG_FILE_NAME="config.yaml"
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

#defining schemafile variable
SCHEMA_CONFIG_FILE_NAME="schema.yaml"
SCHEMA_CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,SCHEMA_CONFIG_FILE_NAME)
SCHEMA_COLUMN_KEY = "columns"

#timestamp
CURRENT_TIMESTAMP=get_current_timestamp()

#Training-Pipeline-information
TRAINING_PIPELINE_CONFIG_KEY= "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY= "pipeline_name"
TRAINING_ARTIFIFACT_DIR_NAME_KEY= "artifact_dir"

#dataingestion variables
DATA_INGESTION_CONFIG_KEY= "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR="Data_ingestion"
DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY= "dataset_download_url"
DATA_INGESTION_ZIP_DATA_DIR_KEY= "zip_data_dir"
DATA_INGESTION_RAW_DATA_DIR_KEY= "raw_data_dir"
DATA_INGESTION_INGESTED_DIR_KEY= "ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY= "ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DIR_KEY= "ingested_test_dir"

#data_validation variables
DATA_VALIDATION_CONFIG_KEY= "data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR="Data_validation"
DATA_VALIDATION_SCHEMA_DIR= "schema_dir"
DATA_VALIDATION_SCHEMA_FILE_PATH_KEY= "schema_file_path"
DATA_VALIDATION_REPORT_FILE_NAME_KEY= "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY= "report_page_file_name"

#data_transformation variables

DATA_TRANSFORMATION_CONFIG_KEY= "data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR= "Data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY= "transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY= "transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY= "transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSED_DIR_KEY= "preprocessed_dir"
DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY= "preprocessed_object_file_name"

NUMERICAL_COLUMN_KEY = "numerical_columns"
TARGET_COLUMN_KEY= "target_column"
