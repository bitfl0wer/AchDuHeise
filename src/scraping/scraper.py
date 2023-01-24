import requests, bleach
from bs4 import BeautifulSoup
from typing import List


def bleach_list(list_str: List[str]) -> list:
    """Sanitizes a list of strings with bleach.clean()

    Args:
        list_str (List[str]): A list containing only str elements.

    Returns:
        list: A sanitized list.
    """
    for item in list_str:
        list_str[list_str.index(item)] = bleach.clean(item)
    return list_str


def scrape_heise_article(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    article = {}
    article["title"] = bleach.clean(soup.find("h1").get_text(), strip=True)
    article["authors"] = bleach_list(
        [
            li.get_text()
            for li in soup.find(class_="creator__names").find_all(
                class_="creator__name"
            )
        ]
    )
    try:
        article["date"] = soup.find(class_="a-datetime__date").get_text()
    except AttributeError:
        article["date"] = soup.find(class_="a-datetime__time").get_text()
    article["date"] = bleach.clean(article.get("date"))
    # article["text"] = soup.find(class_="article-content").get_text()
    article["images"] = bleach_list(
        [img["src"] for img in soup.find(class_="article-image").find_all("img")]
    )
    return article
