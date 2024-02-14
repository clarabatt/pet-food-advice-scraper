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


def treated_data():
    df = pd.read_csv("files/2024-02-13_petsmart_products.csv")
    df = df[df["animal_type"] != "Featured Shops"]
    df["animal_type"] = df["animal_type"].apply(lambda x: x.capitalize())
    df["animal_size"] = df["name"].apply(get_animal_size)
    df["animal_lifestage"] = df["name"].apply(get_life_stage)
    return df
