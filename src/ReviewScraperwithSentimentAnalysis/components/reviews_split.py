from ReviewScraperwithSentimentAnalysis.config import Configuration
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from typing import Any
from ReviewScraperwithSentimentAnalysis import logging
import os
from thefuzz import fuzz
from collections import namedtuple
from ReviewScraperwithSentimentAnalysis.constant import (
    COLUMNS_NAME,
    CAMERA_LABELS,
    BATTERY_LABELS,
    DISPLAY_LABELS,
    SPLIT_REVIES_COLUMNS_NAME,
)

from ReviewScraperwithSentimentAnalysis.utils import to_save_pkl

STAGE_NAME = "REVIEWS SPLIT"


class SplitReviews:
    def __init__(self, configuration=Configuration()) -> None:
        self.camera_list, self.display_list , self.battery_list, self.overall_list = (
            [],
            [],
            [],
            [],
        )
        self.review_split_config = configuration.get_review_split_config()

    @staticmethod
    def to_read_csv(csv_file_path: Path, specific_column: list[str] = None):
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"csv file not found {csv_file_path}")
        if specific_column:
            try:
                df = pd.read_csv(csv_file_path, usecols=specific_column)
                return df

            except ValueError as e:
                raise ValueError("columns not found")
        df = pd.read_csv(csv_file_path)
        return df

    def to_split_reviews(self) -> pd.DataFrame:
        csv_file_path = self.review_split_config.review_csv_path
        review_col_name = COLUMNS_NAME[0]
        review_df = self.to_read_csv(
            csv_file_path=csv_file_path, specific_column=[review_col_name]
        )
        reviews_list = pd.Series(review_df.iloc[:, 0]).to_list()
        comma_list, full_list = self.to_split_comma_full(review_list=reviews_list)
        self.updated_list(combine_reviews_list=comma_list + full_list)

    @staticmethod
    def to_split_comma_full(review_list: list[str]) -> tuple[list[Any]]:
        com_li, full_li = [], []
        nothing = [
            (com_li.append(review.split(",")), full_li.append(review.split(".")))
            for review in review_list
        ]
        del nothing
        return (sum(com_li, []), sum(full_li, []))

    def _helper_updated_list(self, review: str):
        if review:
            if "camera" in review:
                self.camera_list.append(review)
            elif "battery" in review:
                self.battery_list.append(review)
            elif "display" in review:
                self.display_list.append(review)
            else:
                self.overall_list.append(review)

    def updated_list(self, combine_reviews_list: list[str]) -> None:
        for review in combine_reviews_list:
            self._helper_updated_list(review=review)

    @staticmethod
    def to_remove_duplicates(
        duplicate_review_list: list[str], similarity_score: float = 75.0
    ):
        duplicate_review_list_copy = duplicate_review_list.copy()
        to_return_min_len = lambda sen1, sen2: sen1 if len(sen1) > len(sen2) else sen2
        for i in duplicate_review_list_copy:
            for j in duplicate_review_list_copy:
                if i != j and fuzz.partial_ratio(i, j) > similarity_score:
                    try:
                        duplicate_review_list_copy.remove(j)
                    except:
                        pass

        return duplicate_review_list_copy

    def combine_all(self):
        self.to_split_reviews()
        battery_file_path = self.review_split_config.battery_file_name
        camera_file_path = self.review_split_config.camera_file_name
        ovelall_file_path = self.review_split_config.overall_file_name
        display_file_path = self.review_split_config.display_file_name

        file_paths = [
            battery_file_path,
            display_file_path,
            ovelall_file_path,
            camera_file_path,
        ]
        contents = [
            self.to_remove_duplicates(self.battery_list),
            self.to_remove_duplicates(self.display_list),
            self.to_remove_duplicates(self.overall_list),
            self.to_remove_duplicates(self.camera_list),
        ]
        columns_name = SPLIT_REVIES_COLUMNS_NAME
        to_save_pkl(contents=contents, file_paths=file_paths, columns_name=columns_name)


if __name__ == "__main__":
    logging.info(msg=f"<<<<<< START {STAGE_NAME}  >>>>>>")
    split_reviews = SplitReviews()
    split_reviews.combine_all()
    logging.info(msg=f"<<<<<< FINISH {STAGE_NAME}  >>>>>>")
