import streamlit as st
import numpy as np
from app.sidebar import sidebar
from app.data_transformation import treated_data
from app.correlation import correlation_chart

st.set_page_config(
    page_title="Pet Food Analysis",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="expanded",
)

def weighted_rating(x, w):
    """
    Custom weighted rating calculation.
    - x: Array of ratings.
    - w: Array of weights (number of reviews).
    """
    review_threshold = 300
    weight_modifier = np.where(w < review_threshold, 0.5, 1) * np.log1p(w)
    return np.average(x, weights=weight_modifier)


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

# ---------- Table 1 ----------

col1.markdown("### Expensive brands")
best_price_table_df = (
    filtered_df.groupby("brand")["price_per_kg"]
    .mean()
    .sort_values(ascending=False)
    .apply(lambda x: f"${x:.2f}")
    .round(2)
    .head(5)
)
best_price_table_df = best_price_table_df.rename("Price/Kg (avg)")
col1.table(best_price_table_df)
col1.markdown("*\*Price/Kg is a simple average*")
# ---------- Table 2 ----------

col2.markdown("### Best rated brands")
grouped_df = filtered_df.dropna(subset=["rating"])
grouped_df = grouped_df.groupby("brand").filter(lambda x: x['rating_count'].sum() >= 200)
grouped_df = grouped_df.groupby("brand").agg(
    price_per_kg=("price_per_kg", "mean"),
    rating_count=("rating_count", "sum"),
    rating=(
        "rating",
        lambda x: weighted_rating(
            filtered_df.loc[x.index, "rating"],
            filtered_df.loc[x.index, "rating_count"]
        ),
    ),
)

grouped_df = grouped_df.dropna(subset=["price_per_kg"])
grouped_df["price_per_kg"] = grouped_df["price_per_kg"].apply(lambda x: f"${x:.2f}")
grouped_df = grouped_df.sort_values("rating", ascending=False).head(5)
grouped_df = grouped_df.rename(
    columns={"price_per_kg": "Price/Kg (avg)", "rating": "Rating", "rating_count": "# Reviews"}
)
col2.table(grouped_df)
col2.markdown("*\*Rating weighted by number of reviews*")


# ---------- Correlation Chart ----------
st.write("")

st.write("### Correlation Chart")\

fig, correlation_data = correlation_chart(filtered_df)

st.plotly_chart(fig, use_container_width=True)
with st.expander("Notes", expanded=False):
    st.write(
        """
        - **Success**: Products with high ratings and high number of reviews. **Must invest in these products.**
        - **Needs More Marketing**: Products with high ratings but low number of reviews. **Get some of these products.**
        - **Low Quality**: Products with low ratings but high number of reviews. **Avoid these products.**
        - **Question Mark**: Products with low ratings and low number of reviews. **Avoid these products.**
        
        Conclusion:
        - The majority of the products are in the "Needs More Marketing" category. 
        - The lack of products in the "Low Quality" category means that PetSmart must select their products frequently.
        - The "Question Mark" category is the least populated, probably those are recent added products.
        """
    )
    st.download_button(
        label="Download Categorized Products",
        data=correlation_data.to_csv(index=False).encode("utf-8"),
        file_name="categorized_products.csv"
    )
