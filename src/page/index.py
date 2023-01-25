from flask import Blueprint, jsonify
from src.scraping.scraper import scrape_heise_article, Article

index = Blueprint("index", __name__)


@index.route("/", methods=["GET"])
def root():
    article = scrape_heise_article(
        "https://www.heise.de/hintergrund/Finanz-Analyse-Warum-Musks-Twitter-Kauf-so-ein-Desaster-ist-7469162.html"
    )
    article_dict = article.dict()
    return jsonify(article_dict), 200
