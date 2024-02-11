class Variant:
    def __init__(self, size, measureUnit, price, currency, flavor):
        self.size = size
        self.measureUnit = measureUnit
        self.price = price
        self.currency = currency
        self.flavor = flavor


class PetFood:
    def __init__(
        self,
        brand,
        name,
        variants,
        rating,
        category,
        lifeStage,
        heathConsideration,
        petType,
        animalSize,
        description,
    ):
        self.brand = brand
        self.name = name
        self.variants = variants
        self.rating = rating
        self.category = category
        self.lifeStage = lifeStage
        self.heathConsideration = heathConsideration
        self.petType = petType
        self.animalSize = animalSize
        self.description = description
