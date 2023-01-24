import requests
from bs4 import BeautifulSoup


def scrape_heise_article(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    article = {}
    article["title"] = soup.find("h1").get_text()
    article["author"] = soup.find(class_="redakteurskuerzel__link").get_text()
    try:
        article["date"] = soup.find(class_="a-datetime__date").get_text()
    except AttributeError:
        article["date"] = soup.find(class_="a-datetime__time").get_text()
    article["text"] = soup.find(class_="article-content").get_text()
    article["image_urls"] = [img["src"] for img in soup.find_all("img")]
    return article
