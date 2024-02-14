import streamlit as st
import pandas as pd
import numpy as np
from app_sidebar import sidebar
from app_data_transformation import treated_data

st.set_page_config(
    page_title="Pet Food Analysis",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.write("# Pet Food Analysis")

with st.spinner("Running the long computation..."):
    df = treated_data()

sidebar(df)


st.write("")
col1, col2 = st.columns(2)
col1.write(
    "> **Objective:** As a new business owner of pet food subscription service, I want to understand the pet food market and the preferences of pet owners so that I can choose the right products for my business."
)
animal_type = col2.selectbox(
    "Select Animal Type", np.sort(df["animal_type"].unique()), index=2
)
st.divider()
st.write("")

filtered_df = df[df["animal_type"] == animal_type]

col1, col2, col3, col4 = st.columns(4)
col1.metric("\# Products", filtered_df["name"].count())
col2.metric("\# Brands", filtered_df["brand"].nunique())
col3.metric("\# Reviews", filtered_df["rating_count"].sum())
col4.metric("Average Rating", filtered_df["rating"].mean().round(2))
st.write("")

st.bar_chart(data=filtered_df, y=["price", "rating"], x="brand")
