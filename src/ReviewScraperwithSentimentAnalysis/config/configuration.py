import os
from pathlib import Path
from ReviewScraperwithSentimentAnalysis.constant import ARTIFACT_DIR_NAME,DataIngestionConstant,TextPreprocessingConstant
from ReviewScraperwithSentimentAnalysis.utils import read_yaml,make_dirs
from ReviewScraperwithSentimentAnalysis.entity import DataIngestionConfig,TextPreprocessingConfig




class Configuration:
    def __init__(self):
        self.config_content=read_yaml()
        self.artifact_dir_name=ARTIFACT_DIR_NAME
        make_dirs([self.artifact_dir_name])

    def get_data_ingestion_config(self)->DataIngestionConfig:

        data_ingestion_config_content=self.config_content.get(DataIngestionConstant.DATA_INGESTION_ROOT_KEY)
        try:
            root_dir=os.path.join(self.artifact_dir_name,data_ingestion_config_content.get(DataIngestionConstant.DATA_INGESTION_ROOT_DIR_KEY))
            review_file_path=os.path.join(root_dir,data_ingestion_config_content.get(DataIngestionConstant.DATA_INGESTION_FILE_NAME_KEY))
            make_dirs([root_dir])
            data_ingestion_config=DataIngestionConfig(root_dir=root_dir, review_file_path=review_file_path)

            return data_ingestion_config
        except Exception as e:
            raise e

    def get_text_preprocessing_config(self)->TextPreprocessingConfig:


        text_preprocessing_config=self.config_content.get(TextPreprocessingConstant.TEXT_PREPROCESSING_ROOT_KEY)
        root_dir=os.path.join(self.artifact_dir_name,text_preprocessing_config.get(TextPreprocessingConstant.TEXT_PREPROCESSING_ROOT_DIR_KEY))
        make_dirs([root_dir])
        processed_data_file_path=os.path.join(root_dir,TextPreprocessingConstant.TEXT_PREPROCESSING_PREPROCESSED_FILE_PATH_KEY)
        
        text_preprocessing_config=TextPreprocessingConfig(root_dir, processed_data_file_path)
        return text_preprocessing_config
