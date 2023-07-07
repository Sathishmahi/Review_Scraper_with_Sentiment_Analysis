from ReviewScraperwithSentimentAnalysis.config.configuration import Configuration
from ReviewScraperwithSentimentAnalysis.entity.config_entity import *
import os

c = Configuration()

all_expected_out = [
    DataIngestionConfig(
        root_dir="artifact/data_ingestion",
        review_file_path="artifact/data_ingestion/review.csv",
        extract_image_dir_name="artifact/data_ingestion/images",
        extract_product_csv_file_name="artifact/data_ingestion/extract_product.csv",
    ),
    PredictionConfig(
        root_dir="artifact/prediction",
        splited_reviews_dir_path="artifact/review_split/split_review_dir",
        pretrain_model_path="artifact/pretrained_model/hugging_face_model",
        prediction_csv_file_path="artifact/prediction/prediction.csv",
    ),
    PretrainedModelConfig(
        pretrained_model_dir="artifact/pretrained_model/hugging_face_model",
        pretrained_model_name="roberta-large-mnli",
    ),
    ReviewSplitConfig(
        root_dir="artifact/review_split",
        review_csv_path="artifact/data_ingestion/review.csv",
        battery_file_name="artifact/review_split/split_review_dir/battery.pkl",
        display_file_name="artifact/review_split/split_review_dir/display.pkl",
        camera_file_name="artifact/review_split/split_review_dir/camera.pkl",
        overall_file_name="artifact/review_split/split_review_dir/overall.pkl",
        review_split_dir_name="artifact/review_split/split_review_dir",
    ),
    TextPreprocessingConfig(
        root_dir="artifact/text_preprocessing",
        review_file_path="artifact/data_ingestion/review.csv",
        processed_data_file_path="artifact/text_preprocessing/preprocess.csv",
        min_review_len=10,
    ),
    TrainingConfig(
        root_dir="artifact/training",
        model_dir="artifact/training/trained_model",
        model_file_name="artifact/training/trained_model/trained_model.h5",
        data_path="artifact/text_preprocessing/preprocess.csv",
        epochs=1,
        batch_size=64,
        buffer_size=1000,
        vocab_size=1000,
        BiRnnUnits=64,
        eval_data_per=0.25,
        embedding_dim=64,
        no_classes=2,
        output_columns_name="label",
    ),
]

all_expected_dtypes = [
    DataIngestionConfig,
    PredictionConfig,
    PretrainedModelConfig,
    ReviewSplitConfig,
    TextPreprocessingConfig,
    TrainingConfig,
]
all_predicted_out = [
    c.get_data_ingestion_config(),
    c.get_prediciton_config(),
    c.get_pretrained_config(),
    c.get_review_split_config(),
    c.get_text_preprocessing_config(),
    c.get_training_config(),
]

all_predicted_dtypes = all(
    [isinstance(out, dt) for out, dt in zip(all_predicted_out, all_expected_dtypes)]
)


# [DataIngestionConfig(root_dir='artifact/data_ingestion', review_file_path='artifact/data_ingestion/review.csv', extract_image_dir_name='artifact/data_ingestion/images', extract_product_csv_file_name='artifact/data_ingestion/extract_product.csv'),
# PredictionConfig(root_dir='artifact/prediction', splited_reviews_dir_path='artifact/review_split/split_review_dir', pretrain_model_path='pretrained_model/hugging_face_model', prediction_csv_file_path='artifact/prediction/prediction.csv'),
# PretrainedModelConfig(pretrained_model_dir='pretrained_model/hugging_face_model', pretrained_model_name='roberta-large-mnli'), ReviewSplitConfig(root_dir='artifact/review_split', review_csv_path='artifact/data_ingestion/review.csv', battery_file_name='artifact/review_split/split_review_dir/battery.pkl', display_file_name='artifact/review_split/split_review_dir/display.pkl', camera_file_name='artifact/review_split/split_review_dir/camera.pkl', overall_file_name='artifact/review_split/split_review_dir/overall.pkl', review_split_dir_name='artifact/review_split/split_review_dir'), TextPreprocessingConfig(root_dir='artifact/text_preprocessing', review_file_path='artifact/data_ingestion/review.csv', processed_data_file_path='artifact/text_preprocessing/preprocess.csv', min_review_len=10),
# TrainingConfig(root_dir='artifact/training', model_dir='artifact/training/trained_model', model_file_name='artifact/training/trained_model/trained_model.h5', data_path='artifact/text_preprocessing/preprocess.csv', epochs=1, batch_size=64, buffer_size=1000, vocab_size=1000, BiRnnUnits=64, eval_data_per=0.25, embedding_dim=64, no_classes=2, output_columns_name='label')]

# [DataIngestionConfig(root_dir='artifact/data_ingestion', review_file_path='artifact/data_ingestion/review.csv', extract_image_dir_name='artifact/data_ingestion/images', extract_product_csv_file_name='artifact/data_ingestion/extract_product.csv'), PredictionConfig(root_dir='artifact/prediction', splited_reviews_dir_path='artifact/review_split/split_review_dir', pretrain_model_path='pretrained_model/hugging_face_model', prediction_csv_file_path='artifact/prediction/prediction.csv'), PretrainedModelConfig(pretrained_model_dir='pretrained_model/hugging_face_model', pretrained_model_name='roberta-large-mnli'), ReviewSplitConfig(root_dir='artifact/review_split', review_csv_path='artifact/data_ingestion/review.csv', battery_file_name='artifact/review_split/split_review_dir/battery.pkl', display_file_name='artifact/review_split/split_review_dir/display.pkl', camera_file_name='artifact/review_split/split_review_dir/camera.pkl', overall_file_name='artifact/review_split/split_review_dir/overall.pkl', review_split_dir_name='artifact/review_split/split_review_dir'), TextPreprocessingConfig(root_dir='artifact/text_preprocessing', review_file_path='artifact/data_ingestion/review.csv', processed_data_file_path='artifact/text_preprocessing/preprocess.csv', min_review_len=10), TrainingConfig(root_dir='artifact/training', model_dir='artifact/training/trained_model', model_file_name='artifact/training/trained_model/trained_model.h5', data_path='artifact/text_preprocessing/preprocess.csv', epochs=1, batch_size=64, buffer_size=1000, vocab_size=1000, BiRnnUnits=64, eval_data_per=0.25, embedding_dim=64, no_classes=2, output_columns_name='label')]

# print(all_predicted_out)

from ReviewScraperwithSentimentAnalysis.components.prediction import Prediction
from ReviewScraperwithSentimentAnalysis.config.configuration import Configuration
import os

c = Configuration()
prediciton_config = c.get_pretrained_config()
# prediction_csv_file_path = prediciton_config.prediction_csv_file_path
print(prediciton_config)
# print(all_predicted_dtypes)

# print(os.listdir())
