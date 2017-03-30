import datetime as dt
import logging

from peewee import (CharField,
                    TextField,
                    Model,
                    DatabaseError)

from playhouse.sqlite_ext import SqliteExtDatabase
from settings import DATABASE_LOCATION

db = SqliteExtDatabase(DATABASE_LOCATION, journal_mode='WAL')


class BaseModel(Model):

    class Meta:
        database = db


class PostDatabaseError(DatabaseError):
    pass


class PostManager(object):

    def create(self, title, body):
        with db.atomic():
            try:
                post = Post.create(title=title, body=body)
            except Exception as exc:
                logging.exception(exc.message)
                raise PostDatabaseError(exc.message)
        return post

    def search(self, term):
        posts = Post.select().where((Post.title.contains(term)) |
                                    (Post.body.contains(term))).execute()
        return posts

class Post(BaseModel):

    title = CharField(max_length=100, null=False, index=True)
    body = TextField(null=False)

    objects = PostManager()
