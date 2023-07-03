import click
import requests
from selectolax.parser import HTMLParser
from dataclasses import dataclass
from rich import print


@dataclass
class Item:
    name: str
    price: str
    stock: str


def get_data(asin):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0"
    }
    resp = requests.get(f"https://www.amazon.co.uk/dp/{asin}", headers=headers)
    return HTMLParser(resp.text)


def extract_data(html):
    name = html.css_first("h1").text(strip=True)
    price = html.css_first("span.a-offscreen").text(strip=True)
    stock = html.css_first("div#availability").text(strip=True)
    return Item(name, price, stock)


@click.command()
@click.argument("asin")
def scrape(asin):
    html = get_data(asin)
    data = extract_data(html)
    print(data)


if __name__ == "__main__":
    scrape()
