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

    def get(self, _id):
        post = Post.get(Post.id==_id)
        return post

    def create(self, title, body):
        with db.atomic():
            try:
                post = Post.create(title=title, body=body)
            except Exception as exc:
                logging.exception(exc.message)
                raise PostDatabaseError(exc.message)
        return post

    def edit(self, _id, title, body):
        with db.atomic():
            try:
                post = (Post
                        .update(title=title, body=body)
                        .where(Post.id==_id)
                        .execute())
            except Exception as exc:
                logging.exception(exc.message)
                raise PostDatabaseError(exc.message)
        return post

    def paginate(self, page):
        posts = (Post
                 .select(Post.title, Post.id)
                 .order_by(Post.id)
                 .paginate(page=page, paginate_by=10)
                 .execute())
        return posts

    def search(self, term):
        def post_sort(post, term):
            count = post.title.count(term)
            count =+ post.body.count(term)
            return count

        posts = (Post
                 .select()
                 .where( (Post.title.contains(term)) |
                         (Post.body.contains(term)) )
                 .limit(3)
                 .execute())

        posts = sorted([post for post in posts],
                       key=lambda post: post_sort(post, term),
                       reverse=True)
        return posts

class Post(BaseModel):

    title = CharField(max_length=100, null=False, index=True)
    body = TextField(null=False)

    objects = PostManager()
