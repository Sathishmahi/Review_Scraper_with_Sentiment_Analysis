import os
from src.ReviewScraperwithSentimentAnalysis.components.text_preprocessing import TextPreprocessing
from src.ReviewScraperwithSentimentAnalysis.config.configuration import Configuration

c=Configuration()
text_preprocessing_config=c.get_text_preprocessing_config()
review_file_path=text_preprocessing_config.review_file_path
root_dir=os.path.split(review_file_path)[0]

def test_review_preprocessing():

    preprocess = TextPreprocessing()
    preprocess.review_combine_all()

    assert os.path.exists(review_file_path)