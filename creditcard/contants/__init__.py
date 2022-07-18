from datetime import datetime
import os

def get_current_timestamp():
    return f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}"

ROOT_DIR=os.getcwd()
CONFIG_DIR="config_info"
CONFIG_FILE_NAME="config.yaml"
CONFIG_FILE_PATH=os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

#timestamp
CURRENT_TIMESTAMP=get_current_timestamp()

#Training-Pipeline-information
TRAINING_PIPELINE_CONFIG_KEY= "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY= "pipeline_name"
TRAINING_ARTIFIFACT_DIR_NAME_KEY= "artifact_dir"

#dataingestion variables
DATA_INGESTION_CONFIG_KEY= "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR="data_ingestion"
DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY= "dataset_download_url"
DATA_INGESTION_ZIP_DATA_DIR_KEY= "zip_data_dir"
DATA_INGESTION_RAW_DATA_DIR_KEY= "raw_data_dir"
DATA_INGESTION_INGESTED_DIR_KEY= "ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY= "ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DIR_KEY= "ingested_test_dir"