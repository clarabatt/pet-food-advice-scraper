import plotly.express as px
import numpy as np


def correlation_chart(df):
    conditions = [
        (df["rating"] >= 4) & (df["rating_count"] > 300),
        (df["rating"] >= 4) & (df["rating_count"] <= 300),
        (df["rating"] < 4) & (df["rating_count"] > 300),
        (df["rating"] < 4) & (df["rating_count"] <= 300),
    ]

    choices = ["Success", "Needs More Marketing", "Low Quality", "Question Mark"]

    df["Category"] = np.select(conditions, choices, default="Not Categorized")

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

    return fig
