import pandas as pd


def get_life_stage(name: str):
    if "puppy" in name.lower():
        return "puppy"
    elif "kitten" in name.lower():
        return "kitten"
    elif "senior" in name.lower():
        return "senior"
    else:
        return "adult"


def get_animal_size(name: str):
    if "x-small" in name.lower():
        return "x-small"
    elif "x-large" in name.lower():
        return "x-large"
    elif "small" in name.lower():
        return "small"
    elif "medium" in name.lower():
        return "medium"
    elif "large" in name.lower():
        return "large"
    elif "giant" in name.lower():
        return "giant"
    else:
        return None


def treat_data():
    df = pd.read_csv("files/2024-02-13_petsmart_products.csv")
    df["animal_size"] = df["name"].apply(get_animal_size)
    df["animal_lifestage"] = df["name"].apply(get_life_stage)
    return df


treat_data()
