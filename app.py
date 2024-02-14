import streamlit as st
import pandas as pd
from app_sidebar import sidebar

df = pd.read_csv("files/2024-02-13_petsmart_products.csv")

st.write("# Pet Food Analysis")

st.write(
    "> **Objective:** As a new business owner of pet food subscription service, I want to understand the pet food market and the preferences of pet owners so that I can choose the right products for my business."
)

sidebar(df)

animal_type = st.selectbox("Select Animal Type", df["animal_type"].unique())

filtered_df = df[df["animal_type"] == animal_type]

st.bar_chart(data=filtered_df, y=["price", "rating"], x="brand")
