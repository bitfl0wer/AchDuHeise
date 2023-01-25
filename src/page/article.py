from flask import Blueprint, jsonify, render_template, request
from src.scraping.scraper import scrape_article, Article

article = Blueprint("article", __name__)
