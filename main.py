import json
from time import sleep
from scraper.product_fetch import (
    fetch_product_data,
)

# from scraper.petsmart_products_urls import (
#     extract_and_save_all_product_urls,
# )

# extract_and_save_all_product_urls()


def getting_product_data(file_path):
    with open(file_path, "r") as file:
        product_urls = json.load(file)

    data = product_urls["data"]

    for url_array in data.values():
        for url in url_array:
            fetch_product_data(url)
            sleep(1)


getting_product_data("files/2024-02-11_9095_product_urls.json")
