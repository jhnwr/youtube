import requests
from rich import print
from urllib.parse import urljoin
import time
import os


class Client(requests.Session):
    def __init__(self, token, store) -> None:
        super().__init__()
        self.token = token
        self.store = store
        self.baseurl = f"https://{self.store}.myshopify.com/admin/api/2023-01/"
        self.headers.update(
            {"X-Shopify-Access-Token": self.token}
        )

        def rate_hook(r, *args, **kwargs):
            if "X-Shopify-Shop-Api-Call-Limit" in r.headers:
                print("rate:", r.headers["X-Shopify-Shop-Api-Call-Limit"])
            if r.status_code == 429:
                time.sleep(int(float(r.headers["Retry-After"])))
                print("rate limit reached, sleeping")

        self.hooks["response"].append(rate_hook)

    def request(self, method, url, *args, **kwargs):
        return super().request(method, urljoin(self.baseurl, url), *args, **kwargs)


if __name__ == "__main__":
    client = Client(token=os.environ.get("SHOPIFY_API_KEY"), store="jhnwr")
    resp = client.get("products/7360092078278.json?fields=id,title")
    print(resp.json())
    resp = client.get("orders.json?status=any")
    print(resp.json())
