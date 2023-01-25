from flask import Blueprint, jsonify, render_template, request
from src.scraping.scraper import scrape_article, Article

index = Blueprint("index", __name__)


""" @index.route("/", methods=["GET"])
def root():
    article = scrape_article(
        "https://www.heise.de/news/Cyber-Angriff-IT-der-TU-Freiberg-weitreichend-lahmgelegt-7469937.html?perbis"
    )

    return jsonify(article.dict()), 200
 """


@index.route("/", methods=["GET"])
def show_index():
    return render_template("index.html"), 200


@index.route("/", methods=["POST"])
def process_form():
    form_data = request.form
