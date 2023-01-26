from flask import Flask
from pathlib import Path
import os
from src.models import dbsql as db
from src.page import index

app = Flask(
    __name__, template_folder=Path("page/templates"), static_folder=Path("page/static")
)

app.config["SECRET_KEY"] = os.urandom(24).hex()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cache.sqlite"
db.init_app(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.register_blueprint(index.index)
    # app.register_blueprint(article.article)
    app.run(port=8080, debug=True)
