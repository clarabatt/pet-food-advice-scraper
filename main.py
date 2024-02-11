import re
import lxml
import requests
from bs4 import BeautifulSoup
from pet_food_advice_scraper import pet_food

PETSMART_BASE_URL = "https://www.petsmart.ca"
PAGE_SIZE = 36

ANIMALS_SUB_URLS = {
    "cat": f"{PETSMART_BASE_URL}/cat/food-and-treats/dry-food/?pmin=0.01&sz={PAGE_SIZE}&start=",
    "dog": f"{PETSMART_BASE_URL}/dog/food/dry-food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
    "fish": f"{PETSMART_BASE_URL}/fish/food-and-care/food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
    "pet_bird": f"{PETSMART_BASE_URL}/bird/food-and-treats/pet-bird-food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
    "wild_bird": f"{PETSMART_BASE_URL}/bird/food-and-treats/wild-bird-food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
    "reptile": f"{PETSMART_BASE_URL}/reptile/food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
    "small_animals": f"{PETSMART_BASE_URL}/small-pet/food-treats-and-hay/food/?pmin=0.01&srule=best-sellers&sz={PAGE_SIZE}&start=",
}


def get_number_from_string(string):
    return re.findall(r"\d+", string)


def get_product_urls(url, page=0, urls=[], max_pages=0):
    print(url + str(page * PAGE_SIZE))
    page_content = requests.get(url + str(page * PAGE_SIZE))
    soup = BeautifulSoup(page_content.content, "lxml")
    number_of_pages = max_pages

    if page == 0:
        number_of_products_text = soup.find("div", class_="results-hits").get_text()
        number_of_products = get_number_from_string(number_of_products_text)[0]
        number_of_pages = int(number_of_products) // PAGE_SIZE + 1

    food_list = soup.find(id="search-result-items")
    food_elements = food_list.find_all("a", class_="name-link")
    new_urls = urls

    for food in food_elements:
        sub_url = food.get("href")
        new_urls.append(PETSMART_BASE_URL + sub_url)

    return (
        get_product_urls(url, page + 1, new_urls, number_of_pages)
        if page < number_of_pages
        else new_urls
    )


cat_results = get_product_urls(ANIMALS_SUB_URLS["cat"])

print(len(cat_results))
