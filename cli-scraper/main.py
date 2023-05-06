import typer
import requests
from selectolax.parser import HTMLParser
from pydantic import BaseModel, validator
from rich import print

# do basic version first then add in pydantic as we go explaining validation
class Asin(BaseModel):
    id: str

    @validator("id")
    def id_len(cls, val):
        if len(val) != 10:
            raise ValueError(f"Asin must be 10 chars, given {val}, {len(val)}")
        return val


class Item(BaseModel):
    asin: Asin
    price: str


app = typer.Typer()


@app.command()
def get_price(asin: str):
    new_asin = Asin(id=asin)
    print(new_asin)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0"
    }
    resp = requests.get("https://amazon.co.uk/dp/" + asin, headers=headers)
    resp.raise_for_status()
    html = HTMLParser(resp.text)
    item = Item(asin=new_asin, price=html.css_first("span.a-offscreen").text().strip())
    print(item.dict())


if __name__ == "__main__":
    app()
