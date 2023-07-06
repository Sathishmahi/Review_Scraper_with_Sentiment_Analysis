import nltk
import string
import os

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from pathlib import Path

from nltk.corpus import stopwords
from nltk.corpus import stopwords
from ReviewScraperwithSentimentAnalysis.constant import DATA_SET_PATH, COLUMNS_NAME
from ReviewScraperwithSentimentAnalysis.config import Configuration
import pandas as pd
from ReviewScraperwithSentimentAnalysis import logging

stem = PorterStemmer()

STAGE_NAME = "TextPreprocessing"


class TextPreprocessing:
    def __init__(self, Configuration=Configuration()):
        self.text_preprocessing_config = Configuration.get_text_preprocessing_config()
        self.processed_data_file_path = (
            self.text_preprocessing_config.processed_data_file_path
        )

    @staticmethod
    def remove_unwanted_columns(csv_path: Path) -> pd.DataFrame:
        """
        this func to remove unwanted columns like zero std column

        Args:
            csv_path (Path): dataframe's csv file path

        Returns:
            pd.DataFrame: after remove all un wanted columns dataframe

        raise:
            FileExistsError: to raise FileExistsError exception if csv file not avaliable
        """
        if not os.path.exists(csv_path):
            raise FileExistsError(f" csv file not found {csv_path}")
        try:
            df = pd.read_csv(csv_path).drop(columns=COLUMNS_NAME[1])
            return df
        except Exception as e:
            raise e

    def to_remove_stop_punctuation(
        self, df: pd.DataFrame, min_review_len: int = 5
    ) -> pd.DataFrame:
        """
        this func to remove stop word,puc etc

        Args:
            df (pd.DataFrame): raw dataframe
            min_review_len (int, optional): min review length in letters. Defaults to 5.

        Returns:
            pd.DataFrame: preprocessed dataframe

        raise:
            Exception: base exception
        """
        try:
            all_punctuation = string.punctuation
            df[COLUMNS_NAME[0]] = df[COLUMNS_NAME[0]].str.lower()
            all_stop = [
                stop.lower()
                for stop in stopwords.words("english")
                if ("no" not in stop) and ("n'" not in stop) and ("won" not in stop)
            ]
            print(df[COLUMNS_NAME[0]])
            df[COLUMNS_NAME[0]] = df[COLUMNS_NAME[0]].apply(
                lambda sen: " ".join(
                    [
                        stem.stem(word)
                        for word in nltk.word_tokenize(sen)
                        if word not in all_punctuation and all_stop
                    ]
                )
            )
            df[COLUMNS_NAME[0]] = df[COLUMNS_NAME[0]].apply(
                lambda s: s.encode("ascii", "ignore").decode()
            )

            df[COLUMNS_NAME[0]] = df[COLUMNS_NAME[0]].apply(
                lambda s: s if len(s) > min_review_len else None
            )

            df.dropna(inplace=True)

            return df
        except Exception as e:
            raise e

    @staticmethod
    def to_save_csv(df: pd.DataFrame, file_path: Path):
        df.to_csv(file_path, index=False)

    def train_combine_all(self, csv_path: Path = Path(DATA_SET_PATH)):
        df = self.remove_unwanted_columns(csv_path)
        df = self.to_remove_stop_punctuation(df)
        self.to_save_csv(df=df, file_path=self.processed_data_file_path)

    def combine_all(self):
        csv_path = self.text_preprocessing_config.review_file_path
        min_review_len = self.text_preprocessing_config.min_review_len
        df = pd.read_csv(csv_path)
        df = self.to_remove_stop_punctuation(df, min_review_len=min_review_len)
        logging.info(
            f" after preprocess the data , dataset save into {self.processed_data_file_path}"
        )
        self.to_save_csv(df=df, file_path=self.processed_data_file_path)


if __name__ == "__main__":
    logging.info(f"<<<<<<    START {STAGE_NAME}    >>>>>>>")
    preprocess = TextPreprocessing()
    preprocess.combine_all()
    logging.info(f"<<<<<<    END {STAGE_NAME}      >>>>>>>")
