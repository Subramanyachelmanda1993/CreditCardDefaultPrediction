from creditcarddefault.entity.config_entity import DataIngestionConfig
import sys,os
from creditcarddefault.exception import CreditCardDefaultException
from creditcarddefault.logger import logging
from creditcarddefault.entity.artifact_entity import DataIngestionArtifact
import tarfile
import shutil
import numpy as np
from six.moves import urllib
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CreditCardDefaultException(e,sys)

    def download_creditcarddefault_data(self) -> str:
        try:
            #extracting remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #folder location to download file
            csv_download_dir = self.data_ingestion_config.csv_download_dir

            if os.path.exists(csv_download_dir):
                os.remove(csv_download_dir)
            
            os.makedirs(csv_download_dir, exist_ok=True)

            creditcarddefault_file_name = os.path.basename(download_url)

            csv_file_path = os.path.join(csv_download_dir, creditcarddefault_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{csv_file_path}]")
            urllib.request.urlretrieve(download_url, csv_file_path)
            logging.info(f"File :[{csv_file_path}] has been downloaded successfully.")
            return csv_file_path

        except Exception as e:
                raise CreditCardDefaultException(e,sys) from e

    def extract_csv_file(self, csv_file_path:str):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os. remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)

            logging.info(f"Extracting csv file: [{csv_file_path}] into dir: [{raw_data_dir}]")
            # with tarfile.open(tgz_file_path) as creditcarddefault_tgz_file_obj:
            #     creditcarddefault_tgz_file_obj.extractall(path=raw_data_dir)
            original = csv_file_path
            target = raw_data_dir
            shutil.copy(original, target)
            logging.info(f"Extraction completed")
  
        except Exception as e:
            raise CreditCardDefaultException(e,sys) from e 


    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_download_dir = self.data_ingestion_config.raw_download_dir

            file_name = os.listdir(raw_download_dir)[0]
            
            creditcarddefault_file_path = os.path.join(raw_download_dir, file_name)


            logging.info(f"Reading csv file: [{creditcarddefault_file_path}]")
            creditcarddefault_data_frame = pd.read_csv(creditcarddefault_file_path)

            # creditcarddefault_data_frame["income_cat"] = pd.cut(
            #     housing_data_frame["median_income"],
            #     bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
            #     labels=[1,2,3,4,5]
            # )
            

            logging.info(f"Splitting data into train and test")
            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            # for train_index,test_index in split.split(housing_data_frame, housing_data_frame["income_cat"]):
            #     strat_train_set = housing_data_frame.loc[train_index].drop(["income_cat"],axis=1)
            #     strat_test_set = housing_data_frame.loc[test_index].drop(["income_cat"],axis=1)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)
            
            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise CreditCardDefaultException(e,sys) from e


    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            tgz_file_path = self.download_creditcarddefault_data()
            self.extract_tgz_file(tgz_file_path=tgz_file_path)
            return self.split_data_as_train_test()
        except Exception as e:
            raise CreditCardDefaultException(e,sys) from e
    


    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")