import sqlalchemy

from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy

dbsql = SQLAlchemy()


class Article(dbsql.Model, SerializerMixin):
    __tablename__ = "articles"
    url = dbsql.Column(dbsql.String(256), primary_key=True)
    title = dbsql.Column(dbsql.String(128))
    subtitle = dbsql.Column(dbsql.String(256))
    content = dbsql.column(dbsql.String(10000))
