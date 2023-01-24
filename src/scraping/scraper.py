import requests, bleach
from bs4 import BeautifulSoup
from typing import List
from src.scraping.formatter import bleach_list

# needs cleanup
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
    text = bleach_list(
        [p.get_text() for p in soup.find(class_="article-content").find_all("p")]
    )
    text_str = str()
    article["images"] = bleach_list(
        [img["src"] for img in soup.find(class_="article-image").find_all("img")]
    )
    return article
