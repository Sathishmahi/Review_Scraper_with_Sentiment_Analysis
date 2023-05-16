from collections import namedtuple


DataIngestionConfig = namedtuple(
    "DataIngestionConfig",
    [
        "root_dir",
        "review_file_path",
        "extract_image_dir_name",
        "extract_product_csv_file_name",
    ],
)

ReviewSplitConfig = namedtuple(
    "ReviewSplitConfig",
    [
        "root_dir",
        "review_csv_path",
        "battery_file_name",
        "display_file_name",
        "camera_file_name",
        "overall_file_name",
        "review_split_dir_name",
    ],
)

TextPreprocessingConfig = namedtuple(
    "TextPreprocessingConfig",
    ["root_dir", "review_file_path", "processed_data_file_path", "min_review_len"],
)

PredictionConfig = namedtuple(
    "PredictionConfig",
    [
        "root_dir",
        "splited_reviews_dir_path",
        "pretrain_model_path",
        "prediction_csv_file_path",
    ],
)

TrainingConfig = namedtuple(
    "TrainingConfig",
    [
        "root_dir",
        "model_dir",
        "model_file_name",
        "data_path",
        "epochs",
        "batch_size",
        "buffer_size",
        "vocab_size",
        "BiRnnUnits",
        "eval_data_per",
        "embedding_dim",
        "no_classes",
        "output_columns_name",
    ],
)

PretrainedModelConfig = namedtuple(
    "PretrainedModelConfig", ["pretrained_model_dir", "pretrained_model_name"]
)
