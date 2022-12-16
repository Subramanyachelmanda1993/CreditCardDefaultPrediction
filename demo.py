import logging
from distutils.command.config import config
from creditcarddefault.pipeline.pipeline import Pipeline
from creditcarddefault.exception import CreditCardDefaultException
from creditcarddefault.logger import logging
from creditcarddefault.config.configuration import Configuration
from creditcarddefault.component.data_transformation import DataTransformation
from creditcarddefault.util.util import read_yaml_file
import os

def main():
    try:
        config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        pipeline.run_pipeline()
        # data_transformation_config = Configuartion().get_data_transformation_config()
        # data_ingestion_config = Configuration()
        # data_ingestion_config.get_data_ingestion_config()
        # print(data_ingestion_config)
        # # pipeline.start()
        # logging.info("main function execution completed.")
    except Exception as e:
        logging.error(f"{e}")
        print(e)


if __name__=="__main__":
    main()