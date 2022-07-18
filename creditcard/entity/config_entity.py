from collections import namedtuple

TrainingPipelineConfig=namedtuple("TrainingPipelineConfig",
["artifact_dir"])

DataIngestionConfig=namedtuple("DataIngestionConfig",
["dataset_download_url","zip_data_dir","raw_data_dir","ingested_dir","ingested_train_dir","ingested_test_dir"])

