from scraper.product_fetch import (
    fetch_product_data,
)

# from scraper.petsmart_products_urls import (
#     extract_and_save_all_product_urls,
# )

# extract_and_save_all_product_urls()

fetch_product_data(
    "https://www.petsmart.ca/fish/food-and-care/food/tetra-tetrafin-goldfish-flakes-17933.html?cgid=300113&fmethod=Browse"
)
