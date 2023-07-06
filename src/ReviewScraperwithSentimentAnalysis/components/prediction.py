import os
from ReviewScraperwithSentimentAnalysis import logging
from ReviewScraperwithSentimentAnalysis.config import Configuration
from ReviewScraperwithSentimentAnalysis.utils import to_load_pkl, to_save_csv
from ReviewScraperwithSentimentAnalysis.constant import (
    FINAL_LABEL_TO_VALUE_DICT,
    CAMERA_LABELS,
    BATTERY_LABELS,
    DISPLAY_LABELS,
    OVERALL_LABELS,
)
from transformers import pipeline

# import pandas as pd
import numpy as np
from pathlib import Path

STAGE_NAME = "Prediction"


class Prediction:
    def __init__(self, configuration=Configuration()) -> None:
        self.prediction_config = configuration.get_prediciton_config()

    @staticmethod
    def return_series_dict(splited_reviews_dir_path: Path) -> dict:
        """
        this function convert splited reviews list to dict and return it

        Args:
            splited_reviews_dir_path (Path): file path of reviews (pkl file path)

        Returns:
            dict: reviews dict

        raise:
            FileNotFoundError: raise FileNotFoundError if splited_reviews_dir dir not found
            ValueError: raise ValueError if splited_reviews_dir is empty
            e: base exception
        """
        if not os.path.exists(splited_reviews_dir_path):
            e = FileNotFoundError(f" splited dir not found {splited_reviews_dir_path} ")
            logging.exception(msg=e)
            raise e
        list_dirs = os.listdir(splited_reviews_dir_path)
        if not len(list_dirs):
            e = ValueError(
                f" splited_reviews_dir is contanin atleast one item {splited_reviews_dir_path} "
            )
            logging.exception(msg=e)
            raise e
        try:
            final_dict = dict()
            for pkl_path, labels in zip(
                list_dirs,
                [OVERALL_LABELS, BATTERY_LABELS, CAMERA_LABELS, DISPLAY_LABELS],
            ):
                combine_pkl_file_path = os.path.join(splited_reviews_dir_path, pkl_path)
                data_series = to_load_pkl(pkl_file_path=Path(combine_pkl_file_path))
                # col=data_series.columns[0]
                final_dict.update({tuple(labels): data_series.to_list()})
            return final_dict
        except Exception as e:
            logging.exception(msg=e)
            raise e

    @staticmethod
    def load_model(model_path: Path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"model dir not found  {model_path}")
        try:
            model = pipeline("zero-shot-classification", model=model_path)
            logging.info(
                msg=f" zero-shot-classification model path =====>  {model_path} "
            )
            return model
        except Exception as e:
            logging.exception(msg=e)
            raise e

    @staticmethod
    def to_return_max_prob(
        analysis_list: list[str], no_labels: int = 2, thersold: float = 0.1
    ) -> int:
        """
        this func to return max prob result
        results:
            1-positive
            0-neutral
            -1-negative

        Args:
            analysis_list (list[str]): list contain good or bad based on review
            no_labels (int, optional): total of label in this case [good , bad]. Defaults to 2.
            thersold (float, optional): diff between pos and negative review thersold
            for ex pos_prob = 0.7 and neg_prob = 0.3 in this case (pos_prob - neg_prob)>thersold so return 1 .Defaults to 0.1.

        Returns:
            int: whether overall reviews positive or negative or neutral
        """
        no_positive_review, no_negative_review = len(
            [1 for rev in analysis_list if "good" in rev]
        ), len([1 for rev in analysis_list if "bad" in rev])
        # print(no_positive_review,no_negative_review)
        total_reviews = no_positive_review + no_negative_review
        if not total_reviews:
            total_reviews = 1
        if (
            abs(
                (no_positive_review / total_reviews)
                - (no_negative_review / total_reviews)
            )
            <= thersold
        ):
            return 0
        elif (no_positive_review / total_reviews) - (
            no_negative_review / total_reviews
        ) > thersold:
            return 1
        return -1

    def final_prediction(
        self,
        model_path: Path,
        reviews_list: list[list[str]],
        candidates_labels: list[tuple[str]],
    ) -> dict:
        """
        this func to predict the all reviews whether review pos or neg using pretrained NLP model

        Args:
            model_path (Path): pretrained model path
            reviews_list (list[list[str]]): overall review list
            candidates_labels (list[tuple[str]]): candidate labels ex:[pos,neg]

        raise:
            Exception , e: base exception
            FileNotFoundError: to raise FileNotFoundError if pretrained model_path not found

        Returns:
            dict: _description_
        """
        final_dict = dict()
        if len(reviews_list) != len(candidates_labels):
            raise Exception(
                f"len candidates_labels and len reviews_list must be equal your reviews_list len is {len(reviews_list)} and candidates_labels len is {len(candidates_labels)} "
            )
        if not os.path.exists(model_path):
            e = FileNotFoundError(f" pretrained  model file not found {model_path}")
            logging.exception(msg=e)
            raise e
        try:
            model = self.load_model(model_path)
            for review_list, candidate_labels in zip(reviews_list, candidates_labels):
                out = model(review_list[0], candidate_labels=list(candidate_labels))
                final_li = [
                    result.get("labels")[np.argmax(result["scores"])] for result in out
                ]

                out_final = self.to_return_max_prob(analysis_list=final_li)
                # category = candidate_labels[0].split(" ")[1]
                if len(candidate_labels[0].split(" ")) > 1:
                    category = candidate_labels[0].split(" ")[1]
                    final_dict.update(
                        {f"{category}": FINAL_LABEL_TO_VALUE_DICT.get(out_final)}
                    )
            return final_dict
        except Exception as e:
            logging.exception(msg=e)
            raise e

    def combine_all(self):
        """
        combine_all func to combine all func
        """
        model_path = self.prediction_config.pretrain_model_path
        splited_reviews_dir_path = self.prediction_config.splited_reviews_dir_path
        prediction_csv_file_path = self.prediction_config.prediction_csv_file_path
        data_dict = self.return_series_dict(Path(splited_reviews_dir_path))
        final_dict = self.final_prediction(
            model_path=Path(model_path),
            reviews_list=data_dict.values(),
            candidates_labels=list(data_dict.keys()),
        )
        to_save_csv(
            all_reviews=final_dict,
            file_path=prediction_csv_file_path,
            index=list(range(len(final_dict))),
        )


if __name__ == "__main__":
    logging.info(f"<<<<<<    START {STAGE_NAME}   >>>>>>>")
    prediction = Prediction()
    prediction.combine_all()
    logging.info(f"<<<<<<    END {STAGE_NAME}     >>>>>>>")
