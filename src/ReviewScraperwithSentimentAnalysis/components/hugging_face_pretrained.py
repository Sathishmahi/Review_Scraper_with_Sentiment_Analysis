from transformers import pipeline
from ReviewScraperwithSentimentAnalysis.config import Configuration
from pathlib import Path


class PreTrained:
    def __init__(self, configuration=Configuration()):
        self.pretrained_config = configuration.get_pretrained_config()

    @staticmethod
    def load_model(model_name: str):
        model = pipeline("zero-shot-classification", model_name)
        return model

    @staticmethod
    def save_model(model, save_model_path: Path):
        model.save_pretrained(save_model_path)

    def combine_all(self):
        model_name = self.pretrained_config.pretrained_model_name
        save_model_path = self.pretrained_config.pretrained_model_dir
        model = self.load_model(model_name=model_name)
        self.save_model(model=model, save_model_path=save_model_path)
