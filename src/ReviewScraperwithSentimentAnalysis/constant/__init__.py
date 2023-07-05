import os
import time
from dataclasses import dataclass


WAIT = 0.3
CONFIG_FILE_PATH = os.path.join("config", "config.yaml")
PARAMS_FILE_PATH = os.path.join("params.yaml")

ARTIFACT_DIR_NAME = "artifact"
LOGGING_DIR_NAME = "logs"
LOGGING_FILE_NAME = "runing_logs.log"
CURRET_TIME_STAMP = time.asctime().replace(" ", "_").replace(":", "_")
DATA_SET_PATH = "flipkart_data.csv"

FINAL_LABEL_TO_VALUE_DICT = {0: "Neutral", 1: "Positive", -1: "Negative"}

COLUMNS_NAME = ["review", "rating"]
EXTRACT_PRODUCT_COLUMNS_NAME = [
    "image_url",
    "model_name",
    "model_details",
    "over_all_reviews",
    "product_cost",
    "product_offer",
    "free_delivery_list",
]
SPLIT_REVIES_COLUMNS_NAME = ["battery", "display", "overall", "camera"]
CAMERA_LABELS, DISPLAY_LABELS, BATTERY_LABELS, OVERALL_LABELS = (
    ["good camera", "bad camera"],
    ["good dispaly", "bad diaplay"],
    ["good battery", "bad battery"],
    ["good", "bad"],
)


###### DATA INGESTION REALATED CONSTANT


@dataclass
class DataIngestionConstant:
    DATA_INGESTION_ROOT_KEY: str = "data_ingestion"
    DATA_INGESTION_ROOT_DIR_KEY: str = "root_dir"
    DATA_INGESTION_TRAIN_FILE_NAME_KEY: str = "train_data_file_name"
    DATA_INGESTION_EXTRACT_FILE_NAME_KEY: str = "extract_review_file_name"
    DATA_INGESTION_EXTRACT_IMAGES_DIR_NAME: str = "extract_img_dir_name"
    DATA_INGESTION_EXTRACT_PRODUCT_FILE_NAME_KEY: str = "extract_product_csv_file_name"


@dataclass
class TextPreprocessingConstant:
    TEXT_PREPROCESSING_ROOT_KEY: str = "text_preprocessing"
    TEXT_PREPROCESSING_ROOT_DIR_KEY: str = "root_dir"
    TEXT_PREPROCESSING_PREPROCESSED_FILE_PATH_KEY: str = "processed_data_file_path"
    TEXT_PREPROCESSING_MIN_REVIEW_LEN_KEY: str = "MIN_REVIEW_LEN"


@dataclass
class PretrainedModelConstant:
    PRETRAINED_ROOT_KEY: str = "pretrained_model"
    PRETRAINED_ROOT_DIR_KEY: str = "root_dir"
    PRETRAINED_MODEL_DIR_KEY: str = "hugging_face_transfromers_model_dir"
    PRETRAINED_MODEL_NAME_KEY: str = "pretrained_model_name"


@dataclass
class ReviewSplitConstant:
    ReviewSplit_ROOT_KEY: str = "review_split"
    ReviewSplit_ROOT_DIR_KEY: str = "root_dir"
    ReviewSplit_DIR_NAME_KEY: str = "review_split_dir_name"
    ReviewSplit_BATTERY_FILE_NAME_KEY: str = "battery_file_name"
    ReviewSplit_DISPLAY_FILE_NAME_KEY: str = "display_file_name"
    ReviewSplit_CAMERA_FILE_NAME_KEY: str = "camera_file_name"
    ReviewSplit_OVERALL_FILE_NAME_KEY: str = "overall_file_name"


@dataclass
class TrainingConstant:
    TRAINING_ROOT_KEY: str = "training"
    TRAINING_ROOT_DIR_KEY: str = "root_dir"
    TRAINING_MODEL_DIR_KEY: str = "model_dir"
    TRAINING_MODEL_FILE_NAME_KEY: str = "model_file_name"
    TRAINING_BATCH_SIZE_KEY: str = "BATCH_SIZE"
    TRAINING_EPOCHS_KEY: str = "EPOCHS"
    TRAINING_BUFFER_SIZE_KEY: str = "BUFFER_SIZE"
    TRAINING_SEQ_LENGTH_KEY: str = "SEQ_LENGTH"
    TRAINING_VOCAB_SIZE_KEY: str = "VOCAB_SIZE"
    TRAINING_EMBEDDING_DIM_KEY: str = "EMBEDDING_DIM"
    TRAINING_BIRNN_UNITS_KEY: str = "BIRNN_UNITS"
    TRAINING_EVALUATION_DATA_PER_KEY: str = "EVALUATION_DATA_PER"
    TRAINING_NO_CLASSES_KEY: str = "NO_OF_CLASSES"
    TRAINING_OUT_COLUMN_NAME_KEY: str = "OUT_PUT_COLUMN_NAME"


@dataclass
class PredictionConstant:
    PREDICTION_ROOT_KEY: str = "prediction"
    PREDICTION_ROOT_DIR_KEY: str = "root_dir"
    PREDICTION_CSV_FILE_PATH_KEY: str = "predeiction_csv_file_path"


@dataclass
class ToExtractImageEtcConstat:
    OVER_ALL_CLASS: str = "_2kHMtA"
    OVER_ALL_ELE_TYPE: str = "div"

    OVER_ALL_REVIEWS_CLASS: str = "_3LWZlK"
    OVER_ALL_REVIEW_ELE_TYPE: str = "div"

    MODEL_NAME_CLASS: str = "_4rR01T"
    MODEL_NAME_ELE_TYPE: str = "div"

    MODEL_DETAILS_CLASS: str = "rgWa7D"
    MODEL_DETAILS__ELE_TYPE: str = "li"

    PRODUCT_IMAGE_CLASS: str = "_396cs4"
    PRODUCT_IMAGE_ELE_TYPE: str = "img"

    PRODUCT_PRICE_CLASS: str = "_30jeq3 _1_WHN1"
    PRODUCT_PRICE_ELE_TYPE: str = "div"

    PRODUCT_OFFER_CLASS: str = "_3Ay6Sb"
    PRODUCT_OFFER_ELE_TYPE: str = "div"

    FREE_DELIVERY_CLASS: str = "_2Tpdn3"
    FREE_DELIVERY_ELE_TYPE: str = "div"

    BANK_OFFER_CLASS: str = "_2Tpdn3"
    BANK_OFFER_ELE_TYPE: str = "div"
