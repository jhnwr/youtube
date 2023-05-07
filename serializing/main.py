import requests
from pydantic import BaseModel, validator
from rich import print


class Variant(BaseModel):
    id: int
    title: str
    sku: str
    price: str

    @validator("sku")
    def sku_length(cls, value):
        required_length = 10
        if len(value) != required_length:
            raise ValueError(f"sku must be {required_length}")
        return value


class Product(BaseModel):
    id: int
    title: str
    variants: list[Variant] = []


def get_data():
    resp = requests.get("https://www.allbirds.co.uk/products.json")
    return resp.json()["products"]


def main():
    products = get_data()
    for product in products:
        item = Product(**product)
        print(item.dict(exclude={"id"}))
        # print(item.variants[0].sku)


if __name__ == "__main__":
    main()
