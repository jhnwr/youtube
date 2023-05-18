import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass
from rich import print
import asyncio


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


def get_page(client, url):
    resp = client.get(url)
    data = HTMLParser(resp.text)
    if data.css_first("li.next"):
        next_page = data.css_first("li.next a").attributes
    else:
        next_page = {"href": None}
    return Response(body_html=data, next_page=next_page)


def parse_links(html):
    links = html.css("article.product_pod h3 a")
    return [link.attrs["href"] for link in links]


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


def check_url_text(value):
    if "catalogue" not in value:
        return "catalogue/" + value
    else:
        return value

# these functions enable the first stage of the async code
# async def async_get_data(client, url):
#     resp = await client.get(url)
#     html = HTMLParser(resp.text)
#     print(detail_page_new(html))


# async def with_async(links):
#     async with httpx.AsyncClient() as client:
#         tasks = []
#         for link in links:
#             tasks.append(async_get_data(client, link))
#         return await asyncio.gather(*tasks)


def main():
    results = []
    base_url = "https://books.toscrape.com/"
    url = "https://books.toscrape.com/"
    client = httpx.Client()
    while True:
        data = get_page(client, url)
        links = [base_url + check_url_text(link) for link in parse_links(data.body_html)]
        # run the async functions
        # asyncio.run(with_async(links))

        for link in links:
            product_page_data = get_page(client, link)
            book_item = detail_page_new(product_page_data.body_html)
            results.append(book_item)
            print(book_item)
        if data.next_page["href"] == None:
            client.close()
            break
        next_page_url = check_url_text(data.next_page["href"])
        url = base_url + str(next_page_url)
    print(results)


if __name__ == "__main__":
    main()
