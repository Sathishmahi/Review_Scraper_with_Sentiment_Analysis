from src.ReviewScraperwithSentimentAnalysis.components.prediction import Prediction
from src.ReviewScraperwithSentimentAnalysis.config.configuration import Configuration
import os

c = Configuration()
prediciton_config = c.get_prediciton_config()
prediction_csv_file_path = prediciton_config.prediction_csv_file_path


def test_prediction():
    prediction = Prediction()
    prediction.combine_all()
    assert os.path.exists(prediction_csv_file_path)
