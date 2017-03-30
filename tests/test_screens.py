import os
import time
import unittest

from playhouse.test_utils import test_database
from peewee import SqliteDatabase
from flask_webtest import TestApp

from app import app
from models.models import Post

test_db = SqliteDatabase(':memory:')


class ScreensTest(unittest.TestCase):

    def setUp(self):
        Post._meta.database = test_db
        self.app = app
        self.testapp = TestApp(self.app)

    def create_testdata(self, no, title='test title {}', body='some body'):
        posts = []
        for number in xrange(no):
            posts.append(Post.create(title=title.format(number),
                                     body=body))
        return posts

    def test_highlight_search_terms(self):
        with test_database(test_db, (Post,)):
            post = self.create_testdata(1, body='lorem ipsum lorem ipsum test, lorem ipsum')[0]

    def test_account_view(self):
        with test_database(test_db, (Post,)):
            self.create_testdata(1)

            resp = self.testapp.get('/post/1')
            self.assertEqual(resp.context['post'].title, 'test title 0')

    def test_account_view_throws_404(self):
        with test_database(test_db, (Post,)):
            resp = self.testapp.get('/post/1', expect_errors=True)
            self.assertEqual(resp.status_code, 404)
