from flask import Blueprint, jsonify
from src.scraping.scraper import scrape_article, Article

index = Blueprint("index", __name__)


@index.route("/", methods=["GET"])
def root():
    article = scrape_article(
        "https://www.heise.de/news/Cyber-Angriff-IT-der-TU-Freiberg-weitreichend-lahmgelegt-7469937.html?perbis"
    )

    return jsonify(article.dict()), 200
