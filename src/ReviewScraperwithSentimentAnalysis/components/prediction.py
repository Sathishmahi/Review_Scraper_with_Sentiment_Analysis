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


class Prediction:
    def __init__(self, configuration=Configuration()) -> None:
        self.prediction_config = configuration.get_prediciton_config()

    @staticmethod
    def return_series_dict(splited_reviews_dir_path: Path) -> dict:
        final_dict = dict()
        list_dirs = os.listdir(splited_reviews_dir_path)
        for pkl_path, labels in zip(
            list_dirs, [OVERALL_LABELS, BATTERY_LABELS, CAMERA_LABELS, DISPLAY_LABELS]
        ):
            combine_pkl_file_path = os.path.join(splited_reviews_dir_path, pkl_path)
            data_series = to_load_pkl(pkl_file_path=combine_pkl_file_path)
            final_dict.update({tuple(labels): data_series.to_list()})
        return final_dict

    @staticmethod
    def load_model(model_path: Path):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"model dir not found  {model_path}")
        model = pipeline("zero-shot-classification", model=model_path)
        return model

    @staticmethod
    def to_return_max_prob(
        analysis_list: list[str], no_labels: int = 2, thersold: float = 0.1
    ) -> int:
        no_positive_review, no_negative_review = len(
            [1 for rev in analysis_list if "good" in rev]
        ), len([1 for rev in analysis_list if "bad" in rev])
        # print(no_positive_review,no_negative_review)
        total_reviews = no_positive_review + no_negative_review

        if (
            abs(
                (no_positive_review / total_reviews)
                - (no_negative_review / total_reviews)
            )
            <= thersold
        ):
            return 0
        if (no_positive_review / total_reviews) - (
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
        final_dict = dict()
        if len(reviews_list) != len(candidates_labels):
            raise Exception(
                f"len candidates_labels and len reviews_list must be equal your reviews_list len is {len(reviews_list)} and candidates_labels len is {len(candidates_labels)} "
            )

        model = self.load_model(model_path)
        for review_list, candidate_labels in zip(reviews_list, candidates_labels):
            out = model(review_list[0], candidate_labels=list(candidate_labels))
            final_li = [
                result.get("labels")[np.argmax(result["scores"])] for result in out
            ]
            out_final = self.to_return_max_prob(analysis_list=final_li)
            category = candidate_labels[0].split(" ")[1]
            final_dict.update({f"{category}": FINAL_LABEL_TO_VALUE_DICT.get(out_final)})
        return final_dict

    def combine_all(self):
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
    prediction = Prediction()
    prediction.combine_all()
