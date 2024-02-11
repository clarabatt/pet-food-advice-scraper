import json
import requests
import random
import logging
from typing import List, Dict
from bs4 import BeautifulSoup
from scraper.utils import (
    get_numbers_from_string,
    save_to_json_into_files,
)

RequestException = requests.exceptions.RequestException

log_format = "%(levelname)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)

PETSMART_BASE_URL = "https://www.petsmart.ca"
PAGE_SIZE = 36

ANIMALS_SUB_URLS = {
    "fish": f"{PETSMART_BASE_URL}/fish/food-and-care/food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
    "pet_bird": f"{PETSMART_BASE_URL}/bird/food-and-treats/pet-bird-food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
    "wild_bird": f"{PETSMART_BASE_URL}/bird/food-and-treats/wild-bird-food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
    "reptile": f"{PETSMART_BASE_URL}/reptile/food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
    "small_animals": f"{PETSMART_BASE_URL}/small-pet/food-treats-and-hay/food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
    "cat": f"{PETSMART_BASE_URL}/cat/food-and-treats/dry-food/?pmin=0.01&sz={PAGE_SIZE}&start=",
    "dog": f"{PETSMART_BASE_URL}/dog/food/dry-food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
}


def _extract_product_urls_from_html(
    url: str, page: int = 0, urls: List[str] = None, max_pages: int = 0
):
    """
    Params: url: str, page: int, urls: List[str], max_pages: int
    Returns: List[str]
    Extracts all product URLs from the List of products HTML's page.
    To handle pagination, it will keep calling itself until it reaches the last page."""

    if urls is None:
        urls = []

    try:
        logging.debug(url + str(page * PAGE_SIZE))

        page_content = requests.get(url + str(page * PAGE_SIZE))
        page_content.raise_for_status()
    except RequestException as e:
        logging.error(f"Request to {url} failed: {e}")
    else:
        soup = BeautifulSoup(page_content.content, "lxml")
        number_of_pages = max_pages

    if page == 0:
        number_of_products_text = soup.find("div", class_="results-hits").get_text()
        number_of_products = get_numbers_from_string(number_of_products_text)[0]
        number_of_pages = int(number_of_products) // PAGE_SIZE + 1

    food_list = soup.find(id="search-result-items")
    food_elements = food_list.find_all("a", class_="name-link")
    new_urls = urls

    for food in food_elements:
        sub_url = food.get("href")
        new_urls.append(PETSMART_BASE_URL + sub_url)

    return (
        _extract_product_urls_from_html(url, page + 1, new_urls, number_of_pages)
        if page < number_of_pages
        else new_urls
    )


def _append_to_json_file(data: Dict, execution_code: str):
    """
    Params: data: Dict, execution_code: str
    Returns: None
    Appends the data to a json file with the given execution_code. If the file doesn't exist, it creates it.
    """
    urls_json = json.dumps(data)
    try:
        return save_to_json_into_files(urls_json, "products_urls", execution_code)
    except Exception as e:
        logging.error(f"Error saving to json: {e}")


def process_all_animals_products_urls():
    """
    Params: None
    Returns: None
    Start point to extracts all products URLs from the Petsmart website and saves it to a json file.
    Generates a random execution code to simulate a session and aggregate all the data from the same execution.
    """
    execution_code = random.randint(1000, 9999)
    for animal_type, url in ANIMALS_SUB_URLS.items():
        urls_dict = {}
        logging.info(f"Getting all {animal_type} products URLs")
        results = _extract_product_urls_from_html(url)
        urls_dict[animal_type] = results
        logging.info(f"Got {len(results)} {animal_type} products")
        _append_to_json_file(urls_dict, execution_code)

    logging.info("Done")
