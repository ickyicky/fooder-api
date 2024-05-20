import requests as r
from dataclasses import dataclass
from logging import getLogger


logger = getLogger(__name__)


class NotFound(Exception):
    pass


class ParseError(Exception):
    pass


@dataclass
class Product:
    name: str
    kcal: float
    fat: float
    protein: float
    carb: float
    fiber: float


def find(bar_code: str) -> Product:
    url = f"https://world.openfoodfacts.org/api/v2/product/{bar_code}.json"
    response = r.get(url)

    if response.status_code == 404:
        raise NotFound()

    try:
        data = response.json()

        name = data["product"]["product_name"]

        if data["product"]["brands"]:
            name = data["product"]["brands"] + " " + name

        return Product(
            name=name,
            kcal=data["product"]["nutriments"]["energy-kcal_100g"],
            fat=data["product"]["nutriments"]["fat_100g"],
            protein=data["product"]["nutriments"]["proteins_100g"],
            carb=data["product"]["nutriments"]["carbohydrates_100g"],
            fiber=data["product"]["nutriments"].get("fiber_100g", 0.0),
        )
    except Exception as e:
        raise e
        logger.error(e)
        raise ParseError()
