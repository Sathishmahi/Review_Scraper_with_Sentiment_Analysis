from src.ReviewScraperwithSentimentAnalysis.components.data_ingestion_single import (
    toExtractReviewsSingle,
)
from src.ReviewScraperwithSentimentAnalysis.config.configuration import Configuration
import streamlit as st
import subprocess
import pandas as pd
import os

product_name = st.text_input(label="enter the product name")
is_click = st.button(label="predict")
prediction_csv_file_path = (
    Configuration().get_prediciton_config().prediction_csv_file_path
)

if is_click:
    toExtractReviewsSingle(searchString=product_name)
    command = "dvc repro"  # Replace with your desired command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.returncode)
    if result.returncode:
        raise Exception(f"somthing went wrong in run commend  {command}")

    if not os.path.exists(prediction_csv_file_path):
        raise FileNotFoundError(
            f"prediction csv file not fount {prediction_csv_file_path}"
        )
    df = pd.read_csv(prediction_csv_file_path)
    st.dataframe(df)
