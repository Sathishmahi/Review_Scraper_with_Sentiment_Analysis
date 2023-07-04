import streamlit as st
import pandas as pd

path = "/config/workspace/artifact/data_ingestion/extract_product.csv"
df = pd.read_csv(path)
# st.title('A title with _italics_ :blue[colors] and emojis :sunglasses:')
# st.markdown(df.to_html(render_links=True),unsafe_allow_html=True)
# st.dataframe(df)
# st.checkbox("Use container width", value=False, key="use_container_width")

# df = load_data()

# Display the dataframe and allow the user to stretch the dataframe
# across the full width of the container, based on the checkbox value
# st.dataframe(df, use_container_width=st.session_state.use_container_width)

# with open("flower.png", "rb") as file:
#     btn = st.download_button(
#             label="Download image",
#             data=file,
#             file_name="flower.png",
#             mime="image/png"
#           )


st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
