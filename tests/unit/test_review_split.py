import os
from src.ReviewScraperwithSentimentAnalysis.components.reviews_split import SplitReviews
from src.ReviewScraperwithSentimentAnalysis.config.configuration import Configuration

c = Configuration()
review_split_config = c.get_review_split_config()


def test_review_split():
    split_reviews = SplitReviews()
    split_reviews.combine_all()
    review_split_dir_name = review_split_config.review_split_dir_name

    assert os.path.exists(review_split_dir_name) == 1
    assert len(os.listdir(review_split_dir_name)) >= 1
