from src.ReviewScraperwithSentimentAnalysis.components.data_ingestion_single import (
    toExtractReviewsSingle,
)
from src.ReviewScraperwithSentimentAnalysis.components.hugging_face_pretrained import (
    PreTrained,
)
from src.ReviewScraperwithSentimentAnalysis.config.configuration import Configuration
from src.ReviewScraperwithSentimentAnalysis.constant import EXTRACT_PRODUCT_COLUMNS_NAME
import streamlit as st
from pathlib import Path
import subprocess
import pandas as pd
import os
import sys
from src.ReviewScraperwithSentimentAnalysis import logging

product_name = st.text_input(label=" enter the product name ")
st.markdown("\n")
logging.info(msg=f"product name === {product_name}")
is_click = st.button(label="Predict", key="key_1")
st.markdown("\n")

c = Configuration()
prediction_csv_file_path = Path(c.get_prediciton_config().prediction_csv_file_path)
extract_product_csv_file_path = Path(
    c.get_data_ingestion_config().extract_product_csv_file_name
)
review_csv_file_path = Path(c.get_data_ingestion_config().review_file_path)
pretrain = PreTrained()

read_csv_encode = lambda fp: pd.read_csv(fp)


@st.cache_data
def convert_df(fp: Path):
    if not os.path.exists(fp):
        raise FileNotFoundError(f" csv file not found {fp}")
    df = pd.read_csv(fp)
    return df.to_csv(index=False).encode("utf-8")


if is_click:
    try:
        # print("inside the btn")
        toExtractReviewsSingle(searchString=product_name)
        pretrain.combine_all()
        # print("succesfully review extract")
    except Exception as e:
        st.write(f" somthing went wrong please check product name right or wrong ! ")
        logging.exception(msg=e)
        sys.exit()
    # is_click.state = False
    # product_name.
    command = "dvc repro"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stderr)
    if result.returncode:
        st.write(f"somthing went wrong")
        logging.exception(msg=f"somthing wrong result returncode {result.returncode}")
        sys.exit()

    if not os.path.exists(prediction_csv_file_path) or not os.path.exists(
        path=extract_product_csv_file_path
    ):
        msg = f"prediction csv file not fount {prediction_csv_file_path}"
        logging.exception(msg=msg)
        raise FileNotFoundError(msg)

    df = pd.read_csv(prediction_csv_file_path)
    df = df.drop_duplicates().to_markdown()
    # print(df)
    st.write("Product Sentiments")
    st.markdown("\n")
    st.markdown(df)
    st.markdown("\n\n")
    st.write(f"{product_name} varients details")
    df_extract = pd.read_csv(extract_product_csv_file_path)
    df_extract = df_extract.drop_duplicates()
    st.dataframe(df_extract)

    st.markdown("\n\n")
    review_csv = convert_df(review_csv_file_path)
    st.download_button(
        "Download Product Reviews CSV",
        review_csv,
        "reviews.csv",
        "text/csv",
        key="download-csv-reviews",
    )

    logging.info(msg=f"\n\n ALL PIPELINE RUN SUCESSFULLY ")
