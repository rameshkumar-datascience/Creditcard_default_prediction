from creditcard.config.configuration import Configuration
from creditcard.pipeline.pipeline import Pipeline

conf=Configuration()

#check=conf.get_data_transformation_config()
#print(check)
pipe = Pipeline(conf)
pipe.run_pipeline()