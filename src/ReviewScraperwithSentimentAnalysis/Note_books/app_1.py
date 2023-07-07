import streamlit as st
import pandas as pd

df=pd.read_csv("/config/workspace/artifact/data_ingestion/extract_product.csv")
st.dataframe(df)
st.markdown("\n")
st.write("hello how are you")



