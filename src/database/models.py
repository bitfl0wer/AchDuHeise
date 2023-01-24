import sqlalchemy

from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy

dbsql = SQLAlchemy()


class Article(dbsql.Model, SerializerMixin):
    __tablename__ = "articles"
    id = dbsql.Column(dbsql.String(128), primary_key=True)
    headline = dbsql.Column(dbsql.String(128))
    content = dbsql.column(dbsql.String(10000))
