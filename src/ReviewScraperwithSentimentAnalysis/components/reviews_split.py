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
        self.camera_list, self.display_list, self.battery_list, self.overall_list = (
            [],
            [],
            [],
            [],
        )
        self.review_split_config = configuration.get_review_split_config()

    @staticmethod
    def to_read_csv(
        csv_file_path: Path, specific_column: list[str] = [None]
    ) -> pd.DataFrame:
        """
        this func to read the csv file

        Args:
            csv_file_path (Path): _description_
            specific_column (list[str], optional): _description_. Defaults to [None].

        Raises:
            FileNotFoundError: to raise FileNotFoundError if csv file not found
            ValueError: to raise ValueError if column name not present in dataframe
            Exception: base exception

        Returns:
            pd.DataFrame: dataframe
        """
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"csv file not found {csv_file_path}")
        if specific_column:
            try:
                df = pd.read_csv(csv_file_path, usecols=specific_column)
                return df

            except ValueError as e:
                raise ValueError("columns not found")
        try:
            df = pd.read_csv(csv_file_path)
            return df

        except Exception as e:
            raise e

    def to_split_reviews(self) -> None:
        """
        this func to  split the reviews into multiple part for example to split into commas(,) and full stop(.)

        Returns:
            None

        raise:
            Exception: base exception

        """
        try:
            csv_file_path = self.review_split_config.review_csv_path
            review_col_name = COLUMNS_NAME[0]
            review_df = self.to_read_csv(
                csv_file_path=csv_file_path, specific_column=[review_col_name]
            )
            reviews_list = pd.Series(review_df.iloc[:, 0]).to_list()
            comma_list, full_list = self.to_split_comma_full(review_list=reviews_list)
            self.updated_list(combine_reviews_list=comma_list + full_list)
        except Exception as e:
            raise e

    @staticmethod
    def to_split_comma_full(review_list: list[str]) -> tuple[list[Any]]:
        """
        helper function of to_split_reviews function

        Args:
            review_list (list[str]): full or raw extracted reviews list

        Returns:
            tuple[list[Any]]: after split the review to return comma split list and full stop split list
        """
        com_li, full_li = [], []
        nothing = [
            (com_li.append(review.split(",")), full_li.append(review.split(".")))
            for review in review_list
        ]
        del nothing
        return (sum(com_li, []), sum(full_li, []))

    def _helper_updated_list(self, review: str):
        """
        this helper function this func to split the review based on keyword present in the review

        keywords: (display,battery,camera)

        Args:
            review (str): raw review

        Raises:
            Exception: base exception
        """

        try:
            if review:
                if "camera" in review:
                    self.camera_list.append(review)
                elif "battery" in review:
                    self.battery_list.append(review)
                elif "display" in review:
                    self.display_list.append(review)
                else:
                    self.overall_list.append(review)

        except Exception as e:
            logging.exception(msg=e)
            raise e

    def updated_list(self, combine_reviews_list: list[str]) -> None:
        try:
            for review in combine_reviews_list:
                self._helper_updated_list(review=review)
        except Exception as e:
            logging.exception(msg=e)
            raise e

    @staticmethod
    def to_remove_duplicates(
        duplicate_review_list: list[str], similarity_score: float = 75.0
    ) -> list[str]:
        """
        to remove duplicate reviews using fuzz lib

        Args:
            duplicate_review_list (list[str]): raw reviews list
            similarity_score (float, optional): similarity score for ex two sentence similarity score >= 75.
            to remove the one of the review: Defaults to 75.0.

        Returns:
            list[str]: after remove the dulplicate reviews list
        """
        try:
            duplicate_review_list_copy = duplicate_review_list.copy()
            to_return_min_len = (
                lambda sen1, sen2: sen1 if len(sen1) > len(sen2) else sen2
            )
            for i in duplicate_review_list_copy:
                for j in duplicate_review_list_copy:
                    if i != j and fuzz.partial_ratio(i, j) > similarity_score:
                        try:
                            duplicate_review_list_copy.remove(j)
                        except:
                            pass

            return duplicate_review_list_copy
        except Exception as e:
            logging.exception(msg=e)
            raise e

    def combine_all(self) -> None:
        """
        this func to combine all functions

        Return:
            None

        raise:
            Exception: base exeception
        """
        try:
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
            logging.info(f" all split reviews file paths {file_paths} ")
            contents = [
                self.to_remove_duplicates(self.battery_list),
                self.to_remove_duplicates(self.display_list),
                self.to_remove_duplicates(self.overall_list),
                self.to_remove_duplicates(self.camera_list),
            ]
            columns_name = SPLIT_REVIES_COLUMNS_NAME
            to_save_pkl(
                contents=contents, file_paths=file_paths, columns_name=columns_name
            )

        except Exception as e:
            raise e


if __name__ == "__main__":
    logging.info(msg=f"<<<<<< START {STAGE_NAME}  >>>>>>")
    split_reviews = SplitReviews()
    split_reviews.combine_all()
    logging.info(msg=f"<<<<<< FINISH {STAGE_NAME}  >>>>>>")
