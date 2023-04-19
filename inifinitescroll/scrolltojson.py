from playwright.sync_api import sync_playwright
import time
from rich import print


def network_events():
    def check_json(response):
        try:
            if "products" in response.url:
                print({"url": response.url, "data": response.json()})
        except:
            pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 1080})
        page.on("response", lambda response: check_json(response))
        page.goto("https://www.nike.com/gb/w/mens-shoes-nik1zy7ok")
        time.sleep(3)
        page.click("#hf_cookie_text_cookieAccept")
        for x in range(1, 10):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        browser.close()


def main():
    network_events()


if __name__ == "__main__":
    main()
