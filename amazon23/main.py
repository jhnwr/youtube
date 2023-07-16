from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import csv
from dataclasses import dataclass
from rich import print


@dataclass
class Item:
    asin: str
    title: str
    price: str


def get_html(page, asin):
    page.goto(f"https://www.amazon.co.uk/dp/{asin}")
    html = HTMLParser(page.content())
    return html


def parse_html(html, asin):
    item = Item(
        asin=asin,
        title=html.css_first("h1#title").text(strip=True),
        price=html.css_first("span.a-offscreen").text(strip=True),
    )
    return item


def read_csv():
    with open("products.csv", "r") as f:
        reader = csv.reader(f)
        return [item[0] for item in reader]


def run():
    asins = read_csv()
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    page = browser.new_page()
    for asin in asins:
        html = get_html(page, asin)
        print(parse_html(html, asin))

    browser.close()
    pw.stop()


def main():
    run()


if __name__ == "__main__":
    main()
