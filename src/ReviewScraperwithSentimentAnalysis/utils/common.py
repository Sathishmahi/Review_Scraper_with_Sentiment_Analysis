import os
import pandas as pd
import pickle
from pathlib import Path
from ReviewScraperwithSentimentAnalysis.constant import CONFIG_FILE_PATH
from ReviewScraperwithSentimentAnalysis import logging
import yaml


def to_load_pkl(pkl_file_path: Path) -> pd.Series:
    if not os.path.exists(path=pkl_file_path):
        raise FileNotFoundError(f"file not found {pkl_file_path}")
    with open(pkl_file_path, "rb") as pkl_file:
        loaded_data = pickle.load(pkl_file)
    return loaded_data


def make_dirs(dirs_list: list, log_or_not=True):
    try:
        for dir in dirs_list:
            if log_or_not:
                logging.info(f"folder created folder path is {dir}")
            os.makedirs(dir, exist_ok=True)
    except Exception as e:
        logging.exception(e)
        raise e


def read_yaml(yaml_file_path: Path = Path(CONFIG_FILE_PATH)) -> dict:
    try:
        if not os.path.exists(yaml_file_path):
            raise FileNotFoundError("file not found")
        with open(yaml_file_path) as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise e


def to_dataframe(data_dict: dict):
    return pd.DataFrame(data=data_dict)


def to_save_csv(all_reviews, file_path: str, columns_name: list = None, index=None):
    if isinstance(all_reviews, pd.DataFrame):
        all_reviews.to_csv(file_path, index=False)
    if isinstance(all_reviews, list):
        df = pd.DataFrame(all_reviews, columns=columns_name)
    else:
        df = pd.DataFrame(all_reviews, index=index)
        df.to_csv(file_path, index=False)


def to_save_pkl(
    contents: list[list], file_paths: Path, columns_name: list[str] = ["column_1"]
):
    for content, file_path, column_name in zip(contents, file_paths, columns_name):
        data = None
        if isinstance(content, list):
            data = pd.Series({column_name: content})
            with open(file_path, "wb") as pkl_file:
                pickle.dump(data, pkl_file)
                print(len(content))
                print(content)
        else:
            raise Exception(
                f"to_save_pkl content only allowed list not {type(content)} or columns list length  mustbe  equal to contents list"
            )