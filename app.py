from src.ReviewScraperwithSentimentAnalysis.components.data_ingestion_single import (
    toExtractReviewsSingle,
)
from src.ReviewScraperwithSentimentAnalysis.config.configuration import Configuration
from src.ReviewScraperwithSentimentAnalysis.constant import EXTRACT_PRODUCT_COLUMNS_NAME
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
extract_product_csv_file_path=data_ingestion_config=Configuration().get_data_ingestion_config().extract_product_csv_file_name
review_csv_file_path=data_ingestion_config=Configuration().get_data_ingestion_config().review_file_path

read_csv_encode=lambda fp: pd.read_csv(fp).encode("utf-8")

if is_click:
    try:
        # print("inside the btn")
        toExtractReviewsSingle(searchString=product_name)
        # print("succesfully review extract")
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

    if not os.path.exists(prediction_csv_file_path) or not os.path.exists(path=extract_product_csv_file_path):
        msg=f"prediction csv file not fount {prediction_csv_file_path}"
        logging.exception(msg=msg)
        raise FileNotFoundError(
            msg
        )
    
    df = pd.read_csv(prediction_csv_file_path)
    df=df.drop_duplicates().to_markdown()
    # print(df)
    st.markdown(df)
    st.write(f"{product_name} varients details")
    df_extract=pd.read_csv(extract_product_csv_file_path)
    df_extract=df_extract.drop_duplicates()
    df_extract[EXTRACT_PRODUCT_COLUMNS_NAME[0]]=df_extract[EXTRACT_PRODUCT_COLUMNS_NAME[0]].apply(lambda url:f'<a href="{url}" target="_blank">{url}</a>')
    st.markdown(df_extract,unsafe_allow_html=True).to_markdown()
    
 
    df_pre=read_csv_encode(prediction_csv_file_path)
    st.download_button(label="Download Prediction CSV File", data=df_pre, file_name=f"{os.path.splitext(prediction_csv_file_path)[0]}.csv", mime="text/csv")
    
    
    df_rev=read_csv_encode(review_csv_file_path)
    st.download_button(label="Download Reviews CSV File", data=df_rev, file_name=f"{os.path.splitext(review_csv_file_path)[0]}.csv", mime="text/csv")
    
    df_extr=read_csv_encode(extract_product_csv_file_path)
    st.download_button(label="Download Product Varients Details CSV File", data=df_extr, file_name=f"{os.path.splitext(extract_product_csv_file_path)[0]}.csv", mime="text/csv")
    
    logging.info(msg=f'\n\n ALL PIPELINE RUN SUCESSFULLY ')
