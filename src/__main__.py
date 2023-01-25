from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
from os import environ
from src.models import dbsql as db
from src.page import index

load_dotenv()

if "SECRET_KEY" not in environ:
    raise RuntimeError("SECRET_KEY environment variable not set, exiting.")

app = Flask(
    __name__, template_folder=Path("page/templates"), static_folder=Path("page/static")
)

app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cache.sqlite"
db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.register_blueprint(index.index)
    # app.register_blueprint(article.article)
    app.run(port=8080, debug=True)
