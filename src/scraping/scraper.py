import requests, bleach, datetime
from bs4 import BeautifulSoup
from typing import List
from src.scraping.formatter import bleach_list
from dataclasses import dataclass


@dataclass
class Article:
    title: str
    subtitle: str
    content: str
    authors: List[str]
    date: str
    time: str
    image: str

    def dict(self) -> dict:
        """convert an article object into a dictionary

        Returns:
            dict: article as dict
        """
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "content": self.content,
            "authors": self.authors,
            "date": self.date,
            "time": self.time,
            "image": self.image,
        }


# needs cleanup
def scrape_heise_article(url: str) -> Article:
    """takes a heise.de-URL and converts it into an Article-object,
    which contains website-ready data.

    Args:
        url (str): Link to a heise.de-article.

    Returns:
        Article: structured data of type article.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    title = bleach.clean(soup.find("h1").get_text(), strip=True)
    subtitle = str  # TODO
    authors = bleach_list(
        [
            li.get_text()
            for li in soup.find(class_="creator__names").find_all(
                class_="creator__name"
            )
        ]
    )
    try:
        date = soup.find(class_="a-datetime__date").get_text()
    except AttributeError:
        date = soup.find(class_="a-datetime__time").get_text()
    date = bleach.clean(date)
    text = bleach_list(
        [p.get_text() for p in soup.find(class_="article-content").find_all("p")]
    )
    text_str = str()
    images = bleach_list(
        [img["src"] for img in soup.find(class_="article-image").find_all("img")]
    )
    return Article(
        title=title,
        subtitle=subtitle,
        content=text,
        authors=authors,
        date=date,
        time=date,
        image=images[0],
    )
