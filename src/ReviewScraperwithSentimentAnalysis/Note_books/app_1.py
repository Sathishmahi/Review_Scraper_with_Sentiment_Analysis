import streamlit as st
import pandas as pd

if st.button("Download File"):
    df = pd.read_csv("large_df.csv")
    st.download_button(
        label="Click here to download", data=df, file_name="df.csv", mime="text/csv"
    )
