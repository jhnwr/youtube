import httpx
from selectolax.parser import HTMLParser
from rich import print
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    sku: str
    price: str
    special_price: str
    old_price: str
    highlights: list[str] | None


@dataclass
class Response:
    body_html: HTMLParser
    next_page: dict


def get_page(client, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }
    resp = client.get(url, headers=headers)
    html = HTMLParser(resp.text)
    if html.css_first("li a[title=Next]"):
        next_page = html.css_first("li a[title=Next]").attributes
    else:
        next_page = {"href": False}
    return Response(body_html=html, next_page=next_page)


def extract_text(html, selector, index):
    try:
        return html.css(selector)[index].text(strip=True)
    except IndexError:
        return "none"


def parse_product_links(html):
    links = html.css("li.product h3 a")
    return [link.attrs["href"] for link in links]


def parse_detail_page(html):
    highlights = []
    for hlitem in html.css("ul.mb-3 li"):
        highlights.append(hlitem.css_first("li").text(strip=True))

    new_product = Product(
        name=extract_text(html, "title", 0),
        sku=extract_text(html, "span[itemprop=sku]", 0),
        price=extract_text(html, "span.price", 0),
        special_price=extract_text(html, "span.special-price", 0),
        old_price=extract_text(html, "span.save", 0),
        highlights=highlights,
    )
    return new_product


def main():
    client = httpx.Client()
    url = "https://www.cameraworld.co.uk/used-camera-equipment.html?p=1"
    while True:
        html = get_page(client, url)
        links = parse_product_links(html.body_html)
        for link in links:
            new_prod = parse_detail_page(get_page(client, link).body_html)
            print(new_prod)
        if html.next_page["href"] is False:
            client.close()
            print("No more pages")
            break
        else:
            url = html.next_page["href"]


if __name__ == "__main__":
    main()
