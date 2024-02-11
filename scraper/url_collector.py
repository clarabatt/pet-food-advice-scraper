import requests
import random
import logging
from bs4 import BeautifulSoup
from utils.json import append_data_to_json_file
from utils.others import get_numbers_from_string

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


def fetch_all_product_urls_recursively(
    url: str, page: int = 0, urls: list = None, max_pages: int = 0
):
    """
    Recursively fetches and accumulates all product URLs from a paginated list of products on a webpage.
    """

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
        fetch_all_product_urls_recursively(url, page + 1, new_urls, number_of_pages)
        if page < number_of_pages
        else new_urls
    )


def extract_and_save_all_product_urls():
    """
    Extracts all product URLs from the Petsmart website and saves them to a JSON file.
    Generates a random session code to simulate a session and aggregate data.
    """
    description = "All Petsmart DryFood URLs organized by animal type."
    session_code = random.randint(1000, 9999)
    for animal_type, url in ANIMALS_SUB_URLS.items():
        urls_dict = {animal_type: fetch_all_product_urls_recursively(url)}
        logging.info(
            f"Got all {animal_type} product URLs: {len(urls_dict[animal_type])} found"
        )
        append_data_to_json_file(urls_dict, description, session_code, "product_urls")
    logging.info("Data extraction and saving completed.")
