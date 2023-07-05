import os
from src.ReviewScraperwithSentimentAnalysis.components.data_ingestion_single import toExtractReviewsSingle
from src.ReviewScraperwithSentimentAnalysis.config.configuration import Configuration


c=Configuration()
data_ingestion_config=c.get_data_ingestion_config()
review_file_path=data_ingestion_config.review_file_path
extract_image_dir=data_ingestion_config.extract_image_dir_name
extract_product_csv_file_path=data_ingestion_config.extract_product_csv_file_name

def test_data_ingestion_single():
    toExtractReviewsSingle("redminote7s")
    fps=[review_file_path,extract_image_dir,extract_product_csv_file_path]
    assert all([ os.path.exists(fp) for fp in fps ]) == 1