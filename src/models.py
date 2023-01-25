from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy

dbsql = SQLAlchemy()


class CachedArticle(dbsql.Model, SerializerMixin):
    __tablename__ = "articles_cache"
    url = dbsql.Column(dbsql.String(256), primary_key=True)
    title = dbsql.Column(dbsql.String(128))
    subtitle = dbsql.Column(dbsql.String(256))
    authors = dbsql.Column(dbsql.JSON())
    date = dbsql.Column(dbsql.Date())
    time = dbsql.Column(dbsql.Time())
    image = dbsql.Column(dbsql.String())
    content = dbsql.Column(dbsql.String())
    cached_timestamp = dbsql.Column(dbsql.BigInteger())
