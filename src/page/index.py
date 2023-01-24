from flask import Blueprint, jsonify
from src.scraping.scraper import scrape_heise_article

index = Blueprint("index", __name__)


@index.route("/", methods=["GET"])
def root():
    return (
        jsonify(
            scrape_heise_article(
                "https://www.heise.de/hintergrund/Finanz-Analyse-Warum-Musks-Twitter-Kauf-so-ein-Desaster-ist-7469162.html"
            )
        )
    ), 200
