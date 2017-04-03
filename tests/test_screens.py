import os
import time
import unittest

from playhouse.test_utils import test_database
from peewee import SqliteDatabase
from flask_webtest import TestApp

from app import app
from models.models import Post
from views.screens import PostSearchView, SearchForm

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

    def test_post_view(self):
        with test_database(test_db, (Post,)):
            self.create_testdata(1)

            resp = self.testapp.get('/post/1')
            self.assertEqual(resp.context['post'].title, 'test title 0')

    def test_post_view_throws_404(self):
        with test_database(test_db, (Post,)):
            resp = self.testapp.get('/post/1', expect_errors=True)
            self.assertEqual(resp.status_code, 404)

    def test_post_list_view_is_paginated(self):
        with test_database(test_db, (Post,)):
            self.create_testdata(30)

            resp = self.testapp.get('/posts/2')
            self.assertEqual(len(resp.context['posts']), 10)
            self.assertEqual(resp.context['posts'][0].title, 'test title 10')

    def test_highlight_search_terms(self):
        with test_database(test_db, (Post,)):
            post = self.create_testdata(1, body='lorem ipsum lorem ipsum test, lorem ipsum')[0]

            resp = self.testapp.get('/search?q=test')
            self.assertEqual(resp.context['posts'][0].body,
                             '... lorem ipsum <b>test</b>, lorem ipsum ...')

    def test_highlight_search_terms_lacking_words_beginning(self):
        with test_database(test_db, (Post,)):
            post = self.create_testdata(1, body='ipsum test, lorem ipsum')[0]

            resp = self.testapp.get('/search?q=test')
            self.assertEqual(resp.context['posts'][0].body,
                             '... ipsum <b>test</b>, lorem ipsum ...')

    def test_highlight_search_terms_lacking_words_end(self):
        with test_database(test_db, (Post,)):
            post = self.create_testdata(1, body='lorem ipsum test, lorem')[0]

            resp = self.testapp.get('/search?q=test')
            self.assertEqual(resp.context['posts'][0].body,
                             '... lorem ipsum <b>test</b>, lorem ...')

    def test_create_post(self):
        with test_database(test_db, (Post,)):
            params = {
                'title': 'some title',
                'body': 'some body'
            }

            resp = self.testapp.post('/post/create', params=params)
            self.assertEqual(resp.status_code, 302)
            self.assertEqual('/post/' in resp.location, True)

    def test_edit_post(self):
        with test_database(test_db, (Post,)):
            post = self.create_testdata(1, title='test', body='test body')[0]
            params = {
                'title': 'changed title',
                'body': 'changed body'
            }

            resp = self.testapp.put('/post/edit/{}'.format(post.id), params=params)
            changed = Post.objects.get(post.id)

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(changed.title, 'changed title')

    def test_search_no_query_only_gives_form(self):
        resp = self.testapp.get('/search')
        self.assertEqual(resp.context['posts'], None)
        self.assertEqual(isinstance(resp.context['form'], SearchForm), True)


    def test_highlight_search_terms_repeated(self):
        self.fail()
        # with test_database(test_db, (Post,)):
        #     post = self.create_testdata(1, body='ipsum test, lorem ipsum')[0]

        #     resp = self.testapp.get('/search?q=test')
        #     self.assertEqual(resp.context['posts'][0].body,
        #                      '... ipsum <b>test</b>, lorem ipsum ...')
