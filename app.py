import streamlit as st
import pandas as pd
from app_sidebar import sidebar
from app_data_transformation import treated_data

st.write("# Pet Food Analysis")

st.write(
    "> **Objective:** As a new business owner of pet food subscription service, I want to understand the pet food market and the preferences of pet owners so that I can choose the right products for my business."
)

with st.spinner("Running the long computation..."):
    df = treated_data()

sidebar(df)


animal_type = st.selectbox("Select Animal Type", df["animal_type"].unique())

filtered_df = df[df["animal_type"] == animal_type]

st.bar_chart(data=filtered_df, y=["price", "rating"], x="brand")
