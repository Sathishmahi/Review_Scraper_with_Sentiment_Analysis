import os
from pathlib import Path
from ReviewScraperwithSentimentAnalysis.constant import (
    PARAMS_FILE_PATH,
    ARTIFACT_DIR_NAME,
    DataIngestionConstant,
    TextPreprocessingConstant,
    TrainingConstant,
    PretrainedModelConstant,
    ReviewSplitConstant,
    PredictionConstant,
)
from ReviewScraperwithSentimentAnalysis.utils import read_yaml, make_dirs
from ReviewScraperwithSentimentAnalysis.entity import (
    DataIngestionConfig,
    TextPreprocessingConfig,
    TrainingConfig,
    PretrainedModelConfig,
    ReviewSplitConfig,
    PredictionConfig,
)


class Configuration:
    def __init__(self):
        self.config_content = read_yaml()
        self.params_content = read_yaml(yaml_file_path=PARAMS_FILE_PATH)
        self.artifact_dir_name = ARTIFACT_DIR_NAME
        make_dirs([self.artifact_dir_name])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        data_ingestion_config_content = self.config_content.get(
            DataIngestionConstant.DATA_INGESTION_ROOT_KEY
        )
        try:
            root_dir = os.path.join(
                self.artifact_dir_name,
                data_ingestion_config_content.get(
                    DataIngestionConstant.DATA_INGESTION_ROOT_DIR_KEY
                ),
            )
            review_file_path = os.path.join(
                root_dir,
                data_ingestion_config_content.get(
                    DataIngestionConstant.DATA_INGESTION_EXTRACT_FILE_NAME_KEY
                ),
            )
            extract_image_dir_name = os.path.join(
                root_dir,
                data_ingestion_config_content.get(
                    DataIngestionConstant.DATA_INGESTION_EXTRACT_IMAGES_DIR_NAME
                ),
            )
            extract_product_csv_file_name = os.path.join(
                root_dir,
                data_ingestion_config_content.get(
                    DataIngestionConstant.DATA_INGESTION_EXTRACT_PRODUCT_FILE_NAME_KEY
                ),
            )

            make_dirs([root_dir, extract_image_dir_name])

            data_ingestion_config = DataIngestionConfig(
                root_dir=root_dir,
                review_file_path=review_file_path,
                extract_image_dir_name=extract_image_dir_name,
                extract_product_csv_file_name=extract_product_csv_file_name,
            )

            return data_ingestion_config
        except Exception as e:
            raise e

    def get_text_preprocessing_config(self) -> TextPreprocessingConfig:
        text_preprocessing_config = self.config_content.get(
            TextPreprocessingConstant.TEXT_PREPROCESSING_ROOT_KEY
        )
        root_dir = os.path.join(
            self.artifact_dir_name,
            text_preprocessing_config.get(
                TextPreprocessingConstant.TEXT_PREPROCESSING_ROOT_DIR_KEY
            ),
        )

        review_file_path = self.get_data_ingestion_config().review_file_path
        make_dirs([root_dir])
        processed_data_file_path = os.path.join(
            root_dir,
            text_preprocessing_config.get(
                TextPreprocessingConstant.TEXT_PREPROCESSING_PREPROCESSED_FILE_PATH_KEY
            ),
        )

        min_review_len = self.params_content.get(
            TextPreprocessingConstant.TEXT_PREPROCESSING_MIN_REVIEW_LEN_KEY
        )

        text_preprocessing_config = TextPreprocessingConfig(
            root_dir=root_dir,
            processed_data_file_path=processed_data_file_path,
            min_review_len=min_review_len,
            review_file_path=review_file_path,
        )
        return text_preprocessing_config

    def get_prediciton_config(self) -> PredictionConfig:
        prediction_content = self.config_content.get(
            PredictionConstant.PREDICTION_ROOT_KEY
        )
        root_dir = os.path.join(
            self.artifact_dir_name,
            prediction_content.get(PredictionConstant.PREDICTION_ROOT_DIR_KEY),
        )
        splited_reviews_dir_path = self.get_review_split_config().review_split_dir_name
        pretrain_model_path = self.get_pretrained_config().pretrained_model_dir
        predeiction_csv_file_path =os.path.join(root_dir,prediction_content.get(
            PredictionConstant.PREDICTION_CSV_FILE_PATH_KEY
        ))
        make_dirs(dirs_list=[root_dir])

        prediction_config = PredictionConfig(
            root_dir=root_dir,
            splited_reviews_dir_path=splited_reviews_dir_path,
            pretrain_model_path=pretrain_model_path,
            prediction_csv_file_path=predeiction_csv_file_path,
        )

        return prediction_config

    def get_review_split_config(self) -> ReviewSplitConfig:
        review_split_content = self.config_content.get(
            ReviewSplitConstant.ReviewSplit_ROOT_KEY
        )
        root_dir = os.path.join(
            self.artifact_dir_name,
            review_split_content.get(ReviewSplitConstant.ReviewSplit_ROOT_DIR_KEY),
        )

        review_split_dir_path = os.path.join(
            root_dir,
            review_split_content.get(ReviewSplitConstant.ReviewSplit_DIR_NAME_KEY),
        )
        print(review_split_dir_path)
        battery_file_path = os.path.join(
            review_split_dir_path,
            review_split_content.get(
                ReviewSplitConstant.ReviewSplit_BATTERY_FILE_NAME_KEY
            ),
        )
        display_file_path = os.path.join(
            review_split_dir_path,
            review_split_content.get(
                ReviewSplitConstant.ReviewSplit_DISPLAY_FILE_NAME_KEY
            ),
        )
        camera_file_path = os.path.join(
            review_split_dir_path,
            review_split_content.get(
                ReviewSplitConstant.ReviewSplit_CAMERA_FILE_NAME_KEY
            ),
        )
        overall_file_path = os.path.join(
            review_split_dir_path,
            review_split_content.get(
                ReviewSplitConstant.ReviewSplit_OVERALL_FILE_NAME_KEY
            ),
        )

        review_csv_path = self.get_data_ingestion_config().review_file_path
        make_dirs(dirs_list=[Path(root_dir), Path(review_split_dir_path)])

        review_split_config = ReviewSplitConfig(
            root_dir=root_dir,
            review_csv_path=review_csv_path,
            review_split_dir_name=review_split_dir_path,
            battery_file_name=battery_file_path,
            camera_file_name=camera_file_path,
            overall_file_name=overall_file_path,
            display_file_name=display_file_path,
        )

        return review_split_config

    def get_pretrained_config(self) -> PretrainedModelConfig:
        pretrained_config = self.config_content.get(
            PretrainedModelConstant.PRETRAINED_ROOT_KEY
        )
        print(pretrained_config)
        root_dir = pretrained_config.get(
            PretrainedModelConstant.PRETRAINED_ROOT_DIR_KEY
        )
        root_dir_path = os.path.join(self.artifact_dir_name, root_dir)

        pretrained_model_dir = os.path.join(
            root_dir_path,
            pretrained_config.get(PretrainedModelConstant.PRETRAINED_MODEL_DIR_KEY),
        )
        pretrained_model_name = pretrained_config.get(
            PretrainedModelConstant.PRETRAINED_MODEL_NAME_KEY
        )

        make_dirs(dirs_list=[root_dir_path, pretrained_model_dir])

        pretrained_model_config = PretrainedModelConfig(
            pretrained_model_dir=pretrained_model_dir,
            pretrained_model_name=pretrained_model_name,
        )

        return pretrained_model_config

    def get_training_config(self) -> TrainingConfig:
        training_config = self.config_content.get(TrainingConstant.TRAINING_ROOT_KEY)

        root_dir = os.path.join(
            self.artifact_dir_name,
            training_config.get(TrainingConstant.TRAINING_ROOT_DIR_KEY),
        )
        model_dir = os.path.join(
            root_dir, training_config.get(TrainingConstant.TRAINING_MODEL_DIR_KEY)
        )
        model_file_name = os.path.join(
            model_dir,
            training_config.get(TrainingConstant.TRAINING_MODEL_FILE_NAME_KEY),
        )
        data_path = self.get_text_preprocessing_config().processed_data_file_path
        batch_size = self.params_content.get(TrainingConstant.TRAINING_BATCH_SIZE_KEY)
        epochs = self.params_content.get(TrainingConstant.TRAINING_EPOCHS_KEY)
        batch_size = self.params_content.get(TrainingConstant.TRAINING_BATCH_SIZE_KEY)
        buffer_size = self.params_content.get(TrainingConstant.TRAINING_BUFFER_SIZE_KEY)
        vocab_size = self.params_content.get(TrainingConstant.TRAINING_VOCAB_SIZE_KEY)
        BiRnnUnits = self.params_content.get(TrainingConstant.TRAINING_BIRNN_UNITS_KEY)
        eval_data_per = self.params_content.get(
            TrainingConstant.TRAINING_EVALUATION_DATA_PER_KEY
        )
        embedding_dim = self.params_content.get(
            TrainingConstant.TRAINING_EMBEDDING_DIM_KEY
        )
        no_classes = self.params_content.get(TrainingConstant.TRAINING_NO_CLASSES_KEY)
        out_column_name = self.params_content.get(
            TrainingConstant.TRAINING_OUT_COLUMN_NAME_KEY
        )

        training_config = TrainingConfig(
            root_dir,
            model_dir,
            model_file_name,
            data_path,
            epochs,
            batch_size,
            buffer_size,
            vocab_size,
            BiRnnUnits,
            eval_data_per,
            embedding_dim,
            no_classes,
            out_column_name,
        )

        return training_config
