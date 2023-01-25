import requests, bleach, datetime, time
from bs4 import BeautifulSoup
from typing import List
from src.scraping.formatter import (
    bleach_list,
    remove_matching_elements,
    format_string,
    remove_url_parameters,
)
from dataclasses import dataclass
from src.models import CachedArticle
from src.models import dbsql as db


@dataclass
class Article:
    title: str
    subtitle: str
    content: str
    authors: List[str]
    date_article: str
    time_article: str
    image: str
    url: str
    cached_timestamp: int

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
            "date_article": self.date_article,
            "time_article": self.time_article,
            "image": self.image,
            "url": self.url,
            "cached_timestamp": self.cached_timestamp,
        }

    def cache(self) -> None:
        """caches the article by adding it to the database."""
        database_article = CachedArticle(
            url=self.url,
            title=self.title,
            subtitle=self.subtitle,
            authors=self.authors,
            date_article=self.date_article,
            time_article=self.time_article,
            image=self.image,
            content=self.content,
            cached_timestamp=int(time.time()),
        )
        db.session.add(database_article)
        db.session.commit()


def _scrape_authors(soup: BeautifulSoup()) -> str:
    """Scrape authors from a given BeautifulSoup object, which should be a heise.de article.

    Args:
        soup (BeautifulSoup): the BeautifulSoup object to scrape from.

    Returns:
        str: All authors as a string, separated by commas. Format: Firstname Lastname, Firstname Lastname, ...
    """

    authors_list = bleach_list(
        [
            li.get_text()
            for li in soup.find(class_="creator__names").find_all(
                class_="creator__name"
            )
        ]
    )

    authors_str = str()
    for author in authors_list:
        authors_str += f"{author}, "
    return authors_str[:-2]


def _scrape_content(soup: BeautifulSoup()) -> str:

    text_list = bleach_list(
        [p.get_text() for p in soup.find(class_="article-content").find_all("p")]
    )
    text_str = str()
    for element in text_list:
        text_str += f"{element} "
    return format_string(text_str)


def _scrape_date_time(soup: BeautifulSoup()) -> dict:
    output = {"date": None, "time": None}
    date_time = [
        span.get_text() for span in soup.find(class_="a-publish-info__datetime")
    ]

    date_time = remove_matching_elements(date_time, "\n")
    date_time = remove_matching_elements(date_time, "\n    Uhr\n  ")

    if len(date_time) > 1:
        output["time"] = format_string(date_time[1])
        output["date"] = format_string(date_time[0])
    else:
        output["time"] = format_string(date_time[0])
        output["date"] = datetime.date.today().strftime("%d.%m.%Y")

    output["date"] = format_string(output.get("date"))
    return output


def _scrape_image(soup: BeautifulSoup()) -> List[str]:
    return bleach_list(
        [img["src"] for img in soup.find(class_="article-image").find_all("img")]
    )


def _scrape_title(soup: BeautifulSoup()) -> str:
    return format_string(soup.find("h1").get_text())


def _scrape_subtitle(soup: BeautifulSoup()) -> str:
    return format_string(
        format_string(soup.find(class_="a-article-header__lead").get_text())
    )


# and finally...


def scrape_article(url: str) -> Article:
    """takes a heise.de-URL and converts it into an Article-object,
    which contains website-ready data.

    Args:
        url (str): Link to a heise.de-article.

    Returns:
        Article: structured data of type article.
    """
    article = CachedArticle.query.filter(
        CachedArticle.url == remove_url_parameters(url)
    ).one_or_none()
    if article:
        timestamp_curr = int(time.time())
        timestamp_article = int(article.cached_timestamp)
        if not timestamp_curr - timestamp_article > 3600:
            return Article(
                title=article.title,
                subtitle=article.subtitle,
                content=article.content,
                authors=article.authors,
                date_article=article.date_article,
                time_article=article.time_article,
                image=article.image,
                url=article.url,
                cached_timestamp=article.cached_timestamp,
            )

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    article = Article(
        title=_scrape_title(soup),
        subtitle=_scrape_subtitle(soup),
        content=_scrape_content(soup),
        authors=_scrape_authors(soup),
        date_article=_scrape_date_time(soup).get("date"),
        time_article=_scrape_date_time(soup).get("time"),
        image=_scrape_image(soup)[1],
        url=remove_url_parameters(url),
        cached_timestamp=int(time.time()),
    )
    article.cache()
    return article
