from src.ReviewScraperwithSentimentAnalysis.components.data_ingestion_single import (
    toExtractReviewsSingle,
)
from src.ReviewScraperwithSentimentAnalysis.config.configuration import Configuration
import streamlit as st
import subprocess
import pandas as pd
import os
import sys
from src.ReviewScraperwithSentimentAnalysis import logging

product_name = st.text_input(label=" enter the product name ")
logging.info(msg=f'product name === {product_name}')
is_click = st.button(label="Predict",key="key_1")
prediction_csv_file_path = (
    Configuration().get_prediciton_config().prediction_csv_file_path
)

if is_click:
    st.session_state.disabled = False
    try:
        toExtractReviewsSingle(searchString=product_name)
    except Exception as e:
        st.write(f" somthing went wrong please check product name right or wrong ! ")
        logging.exception(msg=e)
        sys.exit()
    # is_click.state = False
    # product_name.
    command = "dvc repro"  
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.returncode)
    if result.returncode:
        st.write(f"somthing went wrong")
        logging.exception(msg=f"somthing wrong result returncode {result.returncode}")
        sys.exit()

    if not os.path.exists(prediction_csv_file_path):
        msg=f"prediction csv file not fount {prediction_csv_file_path}"
        logging.exception(msg=msg)
        raise FileNotFoundError(
            msg
        )
    df = pd.read_csv(prediction_csv_file_path)
    df=df.drop_duplicates()
    st.dataframe(df)
    logging.info(msg=f'\n\n ALL PIPELINE RUN SUCESSFULLY ')
