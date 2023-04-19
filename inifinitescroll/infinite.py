from playwright.sync_api import sync_playwright
import time
from rich import print


def page_down():
    # page down or end works OK here. keyboard option
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size(
                {"width": 1280, "height": 1080}
                )
        page.goto("https://www.nike.com/gb/w/mens-shoes-nik1zy7ok")
        time.sleep(2)
        page.click("#hf_cookie_text_cookieAccept")
        page.wait_for_load_state("networkidle")
        for x in range(1, 5):
            page.keyboard.press("End")
            time.sleep(1)
            print("page down", x)
        browser.close()


def mouse_wheel():
    # scroll with the mouse_wheel
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size(
                {"width": 1280, "height": 1080}
                )
        page.goto("https://www.nike.com/gb/w/mens-shoes-nik1zy7ok")
        time.sleep(2)
        page.click("#hf_cookie_text_cookieAccept")
        page.wait_for_load_state("networkidle")
        for x in range(1, 5):
            page.mouse.wheel(0, 10000)
            print("scrolling", x)
            time.sleep(1)
        browser.close()


def js_eval():
    # evaluate js on the page
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size(
                {"width": 1280, "height": 1080}
                )
        page.goto("https://www.nike.com/gb/w/mens-shoes-nik1zy7ok")
        time.sleep(2)
        page.click("#hf_cookie_text_cookieAccept")
        page.wait_for_load_state("networkidle")
        for x in range(1, 5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            print("eval js", x)
            time.sleep(1)
        browser.close()

def main():
    mouse_wheel()
    time.sleep(1)
    page_down()
    time.sleep(1)
    js_eval()


if __name__ == "__main__":
    main()
