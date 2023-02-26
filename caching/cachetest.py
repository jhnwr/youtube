import requests
import time
from rich import print
from functools import cache


def print_url(r, *args, **kwargs):
    print(r.url)


@cache
def rm_character(char_id):
    resp = requests.get(
        "https://rickandmortyapi.com/api/character/" + str(char_id),
        hooks={"response": print_url},
    )
    return resp.json()


if __name__ == "__main__":
    print(rm_character(42))
    print("---")
    time.sleep(1)
    print(rm_character(42))
