from creditcard.config.configuration import Configuration
from creditcard.pipeline.pipeline import Pipeline

conf=Configuration()

pipe = Pipeline(conf)
pipe.start_data_ingestion()