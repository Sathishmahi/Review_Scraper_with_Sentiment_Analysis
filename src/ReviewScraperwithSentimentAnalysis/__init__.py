import logging
import os
from ReviewScraperwithSentimentAnalysis.constant import *
from ReviewScraperwithSentimentAnalysis.utils import make_dirs


format_str = f" [ %(asctime)s ]   [ %(filename)s    %(funcName)s    %(levelname)s ]    [ %(message)s ]"
file_path = os.path.join(LOGGING_DIR_NAME, f"{CURRET_TIME_STAMP}_{LOGGING_FILE_NAME}")
os.makedirs(os.path.dirname(file_path),exist_ok=True)
logging.basicConfig(filename=file_path, level=logging.INFO, format=format_str)
