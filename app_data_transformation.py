import pandas as pd


def get_life_stage(name: str):
    if "puppy" in name.lower():
        return "Puppy"
    elif "kitten" in name.lower():
        return "Kitten"
    elif "senior" in name.lower():
        return "Senior"
    else:
        return "Adult"


def get_animal_size(name: str):
    if "x-small" in name.lower():
        return "X-Small"
    elif "x-large" in name.lower():
        return "X-Large"
    elif "small" in name.lower():
        return "Small"
    elif "medium" in name.lower():
        return "Medium"
    elif "large" in name.lower():
        return "Large"
    elif "giant" in name.lower():
        return "Giant"
    else:
        return None


def transform_to_kg(row):
    if str(row["size_unit"]).lower() == "lb":
        return row["size_value"] * 0.453592
    if str(row["size_unit"]).lower() == "oz":
        return row["size_value"] * 0.0283495
    if str(row["size_unit"]).lower() == "g":
        return row["size_value"] / 1000
    else:
        return row["size_value"]


def price_per_kg(row):
    if row["price"] is not None and row["weight_kg"] is not None:
        return row["price"] / row["weight_kg"]
    return None


def treated_data():
    df = pd.read_csv("files/2024-02-13_petsmart_products.csv")
    df = df[df["animal_type"] != "Featured Shops"]
    df["animal_type"] = df["animal_type"].apply(lambda x: x.capitalize())
    df["animal_size"] = df["name"].apply(get_animal_size)
    df["animal_lifestage"] = df["name"].apply(get_life_stage)
    df["weight_kg"] = df.apply(transform_to_kg, axis=1)
    df["price_per_kg"] = df.apply(price_per_kg, axis=1)
    return df
