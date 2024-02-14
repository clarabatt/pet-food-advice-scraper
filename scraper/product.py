import os
import csv
from utils.others import get_numbers_from_string, create_files_directory
from datetime import date


class Product:
    def __init__(
        self,
        price: float,
        name: str,
        image: str,
        url: str,
        description: str,
        brand: str,
        rating: float,
        rating_count: int,
        rating_best: float,
        categories: list,
        heath_consideration: str,
        animal_type: str,
        animal_lifestage: str,
        animal_size: str,
        size_merged: str,
    ):
        self.price = price
        self.name = name
        self.url = url
        self.description = description
        self.image = image
        self.brand = brand
        self.rating = rating
        self.rating_count = rating_count
        self.rating_best = rating_best
        self.categories = categories
        self.heath_consideration = heath_consideration
        self.animal_type = animal_type
        self.animal_lifestage = animal_lifestage
        self.animal_size = animal_size
        self.size_value = None
        self.size_unit = None
        self.size_merged = size_merged

        self.separate_size_values()

    def separate_size_values(self):
        num = get_numbers_from_string(self.size_merged)
        if num:
            self.size_value = float(num[0])
            self.size_unit = self.size_merged.replace(num[0], "").strip()
        else:
            self.size_value = None
            self.size_unit = ""

    def append_to_csv(self, file_name: str = "product_data"):
        directory = create_files_directory()
        file_path = os.path.join(directory, f"{date.today()}_{file_name}.csv")

        headers = [
            "price",
            "name",
            "image",
            "url",
            "description",
            "brand",
            "rating",
            "rating_count",
            "rating_best",
            "categories",
            "health_consideration",
            "animal_type",
            "animal_lifestage",
            "animal_size",
            "size_value",
            "size_unit",
            "size_merged",
        ]

        categories_str = "|".join(self.categories)

        file_exists = os.path.exists(file_path)
        need_header = not file_exists or os.stat(file_path).st_size == 0

        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)

            if need_header:
                writer.writeheader()

            product_dict = {
                "price": self.price,
                "name": self.name,
                "image": self.image,
                "url": self.url,
                "description": self.description,
                "brand": self.brand,
                "rating": self.rating,
                "rating_count": self.rating_count,
                "rating_best": self.rating_best,
                "categories": categories_str,
                "health_consideration": self.heath_consideration,
                "animal_type": self.animal_type,
                "animal_lifestage": self.animal_lifestage,
                "animal_size": self.animal_size,
                "size_value": self.size_value,
                "size_unit": self.size_unit,
                "size_merged": self.size_merged,
            }

            writer.writerow(product_dict)
