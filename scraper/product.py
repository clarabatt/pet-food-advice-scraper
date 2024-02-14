class Product:
    def __init__(
        self,
        price: float,
        name: str,
        description: str,
        brand: str,
        rating: float,
        rating_count: int,
        categories: list,
        heath_consideration: str,
        animal_type: str,
        animal_lifestage: str,
        animal_size: str,
    ):
        self.price = price
        self.name = name
        self.description = description
        self.brand = brand
        self.rating = rating
        self.rating_count = rating_count
        self.categories = categories
        self.heath_consideration = heath_consideration
        self.animal_type = animal_type
        self.animal_lifestage = animal_lifestage
        self.animal_size = animal_size
