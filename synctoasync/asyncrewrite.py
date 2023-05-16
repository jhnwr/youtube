import httpx
from selectolax.parser import HTMLParser
import asyncio
from dataclasses import dataclass
from itertools import chain


# could definitely be improved but 7.41 seconds.


@dataclass
class Book:
    title: str
    UPC: str
    product_type: str
    price_inc_tax: str
    price_exc_tax: str
    tax: str
    availability: str
    num_of_reviews: str


@dataclass
class Response:
    body_html: HTMLParser
    next_page: dict


def is_integer(val):
    try:
        return int(val)
    except ValueError:
        return


def parse_detail(html, selector, index):
    try:
        value = html.css(selector)[index].text(strip=True)
        return value
    except:
        return "none"


def detail_page_new(html):
    new_book = Book(
        title=parse_detail(html, "h1", 0),
        UPC=parse_detail(html, "table tbody tr td", 0),
        product_type=parse_detail(html, "table tbody tr td", 1),
        price_inc_tax=parse_detail(html, "table tbody tr td", 2),
        price_exc_tax=parse_detail(html, "table tbody tr td", 3),
        tax=parse_detail(html, "table tbody tr td", 4),
        availability=parse_detail(html, "table tbody tr td", 5),
        num_of_reviews=parse_detail(html, "table tbody tr td", 6),
    )
    return new_book


def get_total_pages(url):
    resp = httpx.get(url)
    html = HTMLParser(resp.text)
    pages = html.css_first("ul.pager li.current").text(strip=True).split()
    pages_int = [is_integer(page) for page in pages if is_integer(page) is not None]
    last_page = max(pages_int)
    return last_page


def parse_links(html):
    links = html.css("article.product_pod h3 a")
    return [link.attrs["href"] for link in links]


async def get_async_links(client, url):
    resp = await client.get(url)
    html = HTMLParser(resp.text)
    links = parse_links(html)
    return links


async def get_links():
    base_url = "https://books.toscrape.com/catalogue/"
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(1, get_total_pages(base_url + "page-1.html") + 1):
            tasks.append(
                asyncio.ensure_future(
                    get_async_links(client, base_url + f"page-{i}.html")
                )
            )
        return await asyncio.gather(*tasks)


async def get_async_details(client, url):
    resp = await client.get(url)
    html = HTMLParser(resp.text)
    print(detail_page_new(html))


async def get_detail(urls):
    base_url = "https://books.toscrape.com/catalogue/"
    async with httpx.AsyncClient() as client:
        tasks = []
        for url in urls:
            tasks.append(
                asyncio.ensure_future(get_async_details(client, base_url + url))
            )
        return await asyncio.gather(*tasks)

def main():
    links = asyncio.run(get_links())
    detail_links = []
    for link in chain(links):
        for l in chain(link):
            detail_links.append(l)
    details = asyncio.run(get_detail(detail_links))
    print(len(details))

if __name__ == "__main__":
   main() 
