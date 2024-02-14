import logging
import requests
import json
from scraper.product import Product
from bs4 import BeautifulSoup

RequestException = requests.exceptions.RequestException


def extract_digital_data_from_scripts(script_tags):
    digital_data = None
    for tag in script_tags:
        if "digitalData" in tag.text:
            try:
                json_str_start = tag.text.find("digitalData = ") + len("digitalData = ")
                json_str_end = tag.text.find("};", json_str_start) + 1
                json_str = tag.text[json_str_start:json_str_end]
                digital_data = json.loads(json_str)
                break
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")
                digital_data = None

    if digital_data is not None:
        logging.info("Successfully extracted digitalData:", digital_data)
        return digital_data
    else:
        logging.error("Could not find or extract digitalData.")
        return None


def extract_product_data_from_html(soup: BeautifulSoup):
    """
    Extracts product data from a product page and saves it into a CSV file.
    """
    script_tags_digital_product = soup.find_all("script", type="text/javascript")
    script_tags_application = soup.find("script", {"type": "application/ld+json"})

    if script_tags_application is None or len(script_tags_digital_product) == 0:
        logging.error(
            "Could not find digitalData or application/ld+json script tags for this product. Skipping."
        )
        return

    product_data_a = json.loads(script_tags_application.string)
    product_data_b = extract_digital_data_from_scripts(script_tags_digital_product)[
        "product"
    ]
    product_data_b = {**product_data_b["productInfo"], **product_data_b["category"]}

    product_data = {**product_data_a, **product_data_b}

    if product_data is not None:
        Product(
            price=product_data["price"],
            name=product_data["productName"],
            description=product_data["description"],
            url=product_data["url"],
            brand=product_data["brand"],
            image=product_data["image"],
            rating=product_data["aggregateRating"]["ratingValue"],
            rating_best=product_data["aggregateRating"]["bestRating"],
            rating_count=product_data["aggregateRating"]["reviewCount"],
            animal_type=product_data["primaryCategory"],
            size_merged=product_data["size"] if "size" in product_data else None,
            categories=[
                product_data["subCategory1"],
                product_data["subCategory2"],
                product_data["subCategory3"],
            ],
            heath_consideration=(
                product_data["healthConsideration"]
                if "healthConsideration" in product_data
                else None
            ),
            animal_lifestage=(
                product_data["lifeStage"] if "lifeStage" in product_data else None
            ),
            animal_size=(
                product_data["animalSize"] if "animalSize" in product_data else None
            ),
        ).append_to_csv("petsmart_products")


def fetch_and_parse_product_page(url: str):
    """
    Fetches product data from a product page and extracts it into a CSV file.
    """
    try:
        page_content = requests.get(url)
        page_content.raise_for_status()
    except RequestException as e:
        logging.error(f"Request to {url} failed: {e}")
    else:
        soup = BeautifulSoup(page_content.content, "lxml")
        extract_product_data_from_html(soup)
