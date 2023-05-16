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


COLUMNS_NAME = ["review", "rating"]
EXTRACT_PRODUCT_COLUMNS_NAME = ["price", "offer", "spec", "details"]
SPLIT_REVIES_COLUMNS_NAME = ["battery", "display", "overall", "camera"]
CAMERA_LABELS, DISPLAY_LABELS, BATTERY_LABELS = (
    ["good camera", "bad camera"],
    ["good dispaly", "bad diaplay"],
    ["good battery", "bad battery"],
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
    TRAINING_EPOCHS_KEY: int = "EPOCHS"
    TRAINING_BUFFER_SIZE_KEY: int = "BUFFER_SIZE"
    TRAINING_SEQ_LENGTH_KEY: int = "SEQ_LENGTH"
    TRAINING_VOCAB_SIZE_KEY: int = "VOCAB_SIZE"
    TRAINING_EMBEDDING_DIM_KEY: int = "EMBEDDING_DIM"
    TRAINING_BIRNN_UNITS_KEY: int = "BIRNN_UNITS"
    TRAINING_EVALUATION_DATA_PER_KEY: float = "EVALUATION_DATA_PER"
    TRAINING_NO_CLASSES_KEY: float = "NO_OF_CLASSES"
    TRAINING_OUT_COLUMN_NAME_KEY: float = "OUT_PUT_COLUMN_NAME"


@dataclass
class ToExtractImageEtcConstat:
    OVER_ALL_CLASS = "_2kHMtA"
    OVER_ALL_ELE_TYPE = "div"

    OVER_ALL_REVIEWS_CLASS = "_3LWZlK"
    OVER_ALL_REVIEW_ELE_TYPE = "div"

    MODEL_NAME_CLASS = "_4rR01T"
    MODEL_NAME_ELE_TYPE = "div"

    MODEL_DETAILS_CLASS = "rgWa7D"
    MODEL_DETAILS__ELE_TYPE = "li"

    PRODUCT_IMAGE_CLASS = "_396cs4"
    PRODUCT_IMAGE_ELE_TYPE = "img"

    PRODUCT_PRICE_CLASS = "_30jeq3 _1_WHN1"
    PRODUCT_PRICE_ELE_TYPE = "div"

    PRODUCT_OFFER_CLASS = "_3Ay6Sb"
    PRODUCT_OFFER_ELE_TYPE = "div"

    FREE_DELIVERY_CLASS = "_2Tpdn3"
    FREE_DELIVERY_ELE_TYPE = "div"

    BANK_OFFER_CLASS = "_2Tpdn3"
    BANK_OFFER_ELE_TYPE = "div"
