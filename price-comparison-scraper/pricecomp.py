import httpx
from selectolax.parser import HTMLParser


def get_data(store, url, selector):
    resp = httpx.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0"
        },
    )
    html = HTMLParser(resp.text)
    price = html.css_first(selector).text().strip()
    return {"store": store, "price": price}


def main():
    results = [
        get_data(
            "Amazon",
            "https://www.amazon.co.uk/dp/B0002E4Z8M",
            "span.a-offscreen"
        ),
        get_data(
            "Thoman",
            "https://www.thomann.de/gb/shure_sm_7b_studiomikro.htm",
            "div.price",
        ),
    ]
    print(results)


if __name__ == "__main__":
    main()
