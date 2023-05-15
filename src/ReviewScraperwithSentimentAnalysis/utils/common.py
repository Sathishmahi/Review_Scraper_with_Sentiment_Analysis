import os
import pandas as pd
from pathlib import Path
from ReviewScraperwithSentimentAnalysis.constant import *
from ReviewScraperwithSentimentAnalysis import logging
import yaml


def make_dirs(dirs_list:list,log_or_not=True):
    try:
        for dir in dirs_list:
            if log_or_not:
                logging.info(f'folder created folder path is {dir}')
            os.makedirs(dir,exist_ok=True)
    except Exception as e:
        logging.exception(e)
        raise e

def read_yaml(yaml_file_path:Path=Path(CONFIG_FILE_PATH))->dict:
    try:
        if not os.path.exists(yaml_file_path):
            raise FileNotFoundError("file not found")
        with open(yaml_file_path) as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise e


def to_dataframe(data_dict:dict):
    
    return pd.DataFrame(data=data_dict)
    

def to_save_csv(all_reviews,file_path:str,columns_name:list=None):
    
    if isinstance(all_reviews, pd.DataFrame):
        all_reviews.to_csv(file_path,index=False)
    if isinstance(all_reviews, list):
        df=pd.DataFrame(all_reviews,columns=columns_name)    
    else:
        df=pd.DataFrame(all_reviews)
        df.to_csv(file_path,index=False)



# make_dirs(['demo'])