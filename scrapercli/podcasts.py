import click
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from rich import print


@dataclass
class Podcast:
    title: str
    link: str
    desc: str
    date: str


def get_data(feed_url):
    pass


def parse_xml(soup):
    pass


@click.command()
@click.argument("feed_url")
def scrape(feed_url):
    pass


if __name__ == "__main__":
    scrape()
