import plotly.express as px
import numpy as np

rating_param = 4
rating_count_param = 300

def correlation_table(df):
    conditions = [
        (df["rating"] >= rating_param) & (df["rating_count"] > rating_count_param),
        (df["rating"] >= rating_param) & (df["rating_count"] <= rating_count_param),
        (df["rating"] < rating_param) & (df["rating_count"] > rating_count_param),
        (df["rating"] < rating_param) & (df["rating_count"] <= rating_count_param),
    ]

    choices = ["Success", "Needs More Marketing", "Low Quality", "Question Mark"]

    df["Category"] = np.select(conditions, choices, default="Not Categorized")

    return df

def correlation_chart(df):
    df = correlation_table(df)

    fig = px.scatter(
        df,
        x="rating_count",
        y="rating",
        color="Category",
        hover_data=["name", "brand", "price_per_kg"],
        title="Product Rating vs. Rating Count Analysis",
    )

    fig.update_layout(
        xaxis_title="Rating Count",
        yaxis_title="Rating",
        legend_title="Product Category",
    )
    
    df_filtered = df[["Category", "name", "brand", "price_per_kg", "rating_count", "rating"]].sort_values("Category", ascending=False).head(5)
    df_filtered = df_filtered.rename(columns={"rating_count": "Rating Count", "rating": "Rating", "price_per_kg": "Price per Kg", "name": "Product Name", "brand": "Brand"})

    return fig, df_filtered

