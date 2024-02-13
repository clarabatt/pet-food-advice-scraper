import logging
import requests
import json
import random
from bs4 import BeautifulSoup
from utils.csv import append_to_csv

RequestException = requests.exceptions.RequestException


def extract_data_from_product_page(soup: BeautifulSoup):
    """
    Extracts product data from a product page and saves it into a CSV file.
    """
    script_tags = soup.find_all("script", type="text/javascript")

    product_data = identify_product_data(script_tags)

    if product_data is not None:
        append_to_csv(product_data["product"], "product_data")


def identify_product_data(script_tags):
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


def fetch_product_data(url: str):
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
        extract_data_from_product_page(soup)
