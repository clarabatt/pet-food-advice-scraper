import streamlit as st
import pandas as pd
import numpy as np
from app_sidebar import sidebar
from app_data_transformation import treated_data
from app_correlation import correlation_chart

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

# ---------- Price per Kg ----------

col1, col2 = st.columns(2)
col1.markdown("### Cheapest brands")
best_price_table_df = (
    filtered_df.groupby("brand")["price_per_kg"]
    .mean()
    .sort_values(ascending=True)
    .apply(lambda x: f"${x:.2f}")
    .round(2)
    .head(5)
)
best_price_table_df = best_price_table_df.rename("Price per Kg")
col1.table(best_price_table_df)
col2.markdown("### Best rated brands")
grouped_df = filtered_df.groupby("brand").agg(
    {
        "price_per_kg": lambda x: np.average(
            x, weights=filtered_df.loc[x.index, "rating"]
        ),
        "rating": "mean",
    }
)

grouped_df = grouped_df.dropna(subset=["price_per_kg"])
grouped_df["price_per_kg"] = grouped_df["price_per_kg"].apply(lambda x: f"${x:.2f}")
grouped_df = grouped_df.sort_values("rating", ascending=False).head(5)
grouped_df = grouped_df.rename(
    columns={"price_per_kg": "Price per Kg", "rating": "Rating"}
)
col2.table(grouped_df)


# ---------- Correlation Chart ----------

st.write("### Correlation Chart")

st.plotly_chart(correlation_chart(filtered_df), use_container_width=True)
st.expander("Notes", expanded=False).write(
    """
    - **Success**: Products with high ratings and high number of reviews.
    - **Needs More Marketing**: Products with high ratings but low number of reviews.
    - **Low Quality**: Products with low ratings but high number of reviews.
    - **Question Mark**: Products with low ratings and low number of reviews.
    
    Conclusion:
    - The majority of the products are in the "Needs More Marketing" category. 
    - The lack of products in the "Low Quality" category means that PetSmart must select their products frequently.
    - The "Question Mark" category is the least populated, propably those are recent added products.
    """
)
