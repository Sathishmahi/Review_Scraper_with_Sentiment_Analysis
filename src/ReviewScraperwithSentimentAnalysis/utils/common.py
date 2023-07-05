import os
import pandas as pd
import pickle
from pathlib import Path
from ReviewScraperwithSentimentAnalysis.constant import CONFIG_FILE_PATH
from ReviewScraperwithSentimentAnalysis import logging
from typing import Any
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
    if not os.path.exists(yaml_file_path):
        raise FileNotFoundError(f"yaml file not found {yaml_file_path}")
    try:
        with open(yaml_file_path) as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise e


def to_dataframe(data_dict: dict):
    if not isinstance(data_dict, dict):
        raise ValueError(f"must be data type is dict you passed {type(data_dict)} ")
    return pd.DataFrame(data=data_dict)


def to_save_csv(
    all_reviews: Any, file_path: str, columns_name: list = [None], index=None
):
    try:
        if isinstance(all_reviews, pd.DataFrame):
            all_reviews.to_csv(file_path, index=False)
        elif isinstance(all_reviews, dict):
            df = pd.DataFrame(data=all_reviews)
            df.to_csv(file_path, index=False)
        elif isinstance(all_reviews[0], list | tuple) and (
            isinstance(all_reviews, list | tuple)
        ):
            if not columns_name[0]:
                columns_name = list(range(len(all_reviews)))
            all_reviews = {cn: data for cn, data in zip(columns_name, all_reviews)}
            df = pd.DataFrame(all_reviews, columns=columns_name)
            df.to_csv(file_path, index=False)
        else:
            df = pd.DataFrame(all_reviews, index=index)
            df.to_csv(file_path, index=False)

    except Exception as e:
        raise e


def to_save_pkl(
    contents: list[list], file_paths: list[Path], columns_name: list[str] = ["column_1"]
):
    try:
        for content, file_path, column_name in zip(contents, file_paths, columns_name):
            data = None
            if isinstance(content, list):
                data = pd.Series({column_name: content})
                with open(file_path, "wb") as pkl_file:
                    pickle.dump(data, pkl_file)
            else:
                raise ValueError(
                    f"to_save_pkl content only allowed list not {type(content)} or columns list length  mustbe  equal to contents list"
                )
    except Exception as e:
        raise e
