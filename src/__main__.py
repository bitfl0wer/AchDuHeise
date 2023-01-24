from flask import Flask
from pathlib import Path
from dotenv import load_dotenv
from os import environ
from src.database.models import dbsql as db

load_dotenv()

if "SECRET_KEY" not in environ:
    raise RuntimeError("SECRET_KEY environment variable not set, exiting.")

app = Flask(
    __name__, template_folder=Path("page/templates"), static_folder=Path("page/static")
)

app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.sqlite"
db.init_app(app)

if __name__ == "__main__":
    db.create_all(app=app)
    app.run(port=8080, debug=True)
