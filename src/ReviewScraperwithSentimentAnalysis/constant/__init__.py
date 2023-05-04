import os
import time
from dataclasses import dataclass


CONFIG_FILE_PATH=os.path.join("config","config.yaml")
PARAMS_FILE_PATH=os.path.join("params.yaml")

ARTIFACT_DIR_NAME="artifact"
LOGGING_DIR_NAME="logging"
LOGGING_FILE_NAME="runing_logs.log"
CURRET_TIME_STAMP=time.asctime().replace(" ", "_").replace(":", "_")
DATA_SET_PATH="flipkart_data.csv"


COLUMNS_NAME=["review","rating"]



###### DATA INGESTION REALATED CONSTANT

@dataclass
class DataIngestionConstant:
    DATA_INGESTION_ROOT_KEY:str="data_ingestion"
    DATA_INGESTION_ROOT_DIR_KEY:str="root_dir"
    DATA_INGESTION_FILE_NAME_KEY:str="file_name"


@dataclass
class TextPreprocessingConstant:
    TEXT_PREPROCESSING_ROOT_KEY:str="text_preprocessing"
    TEXT_PREPROCESSING_ROOT_DIR_KEY:str="root_dir"
    TEXT_PREPROCESSING_PREPROCESSED_FILE_PATH_KEY:str="processed_data_file_path"