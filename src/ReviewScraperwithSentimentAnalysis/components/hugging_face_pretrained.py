from transformers import pipeline
from ReviewScraperwithSentimentAnalysis.config import Configuration
from ReviewScraperwithSentimentAnalysis import logging
from pathlib import Path
import os

STAGE_NAME = "PreTrained"


class PreTrained:
    def __init__(self, configuration=Configuration()):
        self.pretrained_config = configuration.get_pretrained_config()

    @staticmethod
    def load_model(model_name: str):
        """
        func to load the huggingface pretrain model

        Args:
            model_name (str): huggingface model name

        Returns:
            Model: to return pretrain huggingface zero-shot-classification model

        raise:
            Exception: base exception
        """
        try:

            logging.info(f" pretrained model name {model_name} ")
            model = pipeline("zero-shot-classification", model_name)
            return model

        except Exception as e:
            logging.exception(msg=e)
            raise e

    @staticmethod
    def save_model(model, save_model_path: Path)->None:
        """
        this func to save the pretrain HF zero-shot-classification model

        Args:
            model Model: pretrain model
            save_model_path (Path): save model path
        Return: 
            None

        raise:
            Exception: base exception
        """
        try:
            logging.info(f" pretrained model save into {save_model_path} ")
            model.save_pretrained(save_model_path)
        except Exception as e:
            logging.exception(msg=e)
            raise e

    def combine_all(self)->None:
        """
        this func to combine all functions

        Return:
            None
        raise:
            Exception: base exception
        """
        model_name = self.pretrained_config.pretrained_model_name
        save_model_path = self.pretrained_config.pretrained_model_dir
        if not len(os.listdir(save_model_path)):
            model = self.load_model(model_name=model_name)
            self.save_model(model=model, save_model_path=save_model_path)


if __name__ == "__main__":
    logging.info(msg=f" >>>>>>  START {STAGE_NAME}    >>>>>>")
    pretrain = PreTrained()
    pretrain.combine_all()
    logging.info(msg=f" >>>>>>  END {STAGE_NAME}    >>>>>>")