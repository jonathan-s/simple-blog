import datetime as dt
import logging

from peewee import (CharField,
                    TextField,
                    Model)

from playhouse.sqlite_ext import SqliteExtDatabase
from settings import DATABASE_LOCATION

db = SqliteExtDatabase(DATABASE_LOCATION)


class BaseModel(Model):

    class Meta:
        database = db

class PostManager(object):

    def create(self, title, body):
        pass

class Post(BaseModel):

    title = CharField(max_length=100, null=False, index=True)
    body = TextField(max_length=50, null=False)

    objects = PostManager()
