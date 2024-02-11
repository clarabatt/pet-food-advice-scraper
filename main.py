from pet_food_advice_scraper import pet_food
from bs4 import BeautifulSoup
import requests

PETSMART_BASE_URL = "https://www.petsmart.ca"
PETSMART_CAT_DRY_FOOD = (
    "https://www.petsmart.ca/cat/food-and-treats/dry-food/?pmin=0.01&start=24&sz=24"
)
PETSMART_DOG_DRY_FOOD = "https://www.petsmart.ca/dog/food/dry-food/?pmin=0.01&srule=best-sellers&start=24&sz=24"
PETSMART_FISH_DRY_FOOD = "https://www.petsmart.ca/fish/food-and-care/food/?pmin=0.01&srule=best-sellers&start=24&sz=24"


page = requests.get(PETSMART_DOG_DRY_FOOD)
soup = BeautifulSoup(page.content, "html.parser")

food_list = soup.find(id="search-result-items")

food_elements = food_list.find_all("a", class_="name-link")

for food in food_elements:
    sub_url = food.get("href")
    product_url = PETSMART_BASE_URL + sub_url
    print(product_url)
