import unittest
import logging

from playhouse.test_utils import test_database
from peewee import SqliteDatabase
from mock import MagicMock, patch

from models.models import Post, PostDatabaseError

test_db = SqliteDatabase(':memory:')


class PostModelTest(unittest.TestCase):

    def setUp(self):
        pass

    def create_testdata(self, no, title='test title {}', body='some body'):
        for number in xrange(no):
            Post.create(title=title.format(number),
                        body=body)

    def test_create_post_with_manager(self):
        with test_database(test_db, (Post,)):
            post = Post.objects.create(title='test title', body='some body')

            self.assertEqual(post.title, 'test title')
            self.assertEqual(post.body, 'some body')

    @patch('logging.exception')
    def test_create_post_fails_raises_error(self, mock_logg):
        with self.assertRaises(PostDatabaseError):
            post = Post.objects.create(title='test title', body='some body')

        self.assertEqual(mock_logg.called, True)

    def test_create_post_with_weird_unicode(self):
        pass

    def test_search_finds_term_in_title(self):
        with test_database(test_db, (Post,)):
            self.create_testdata(1, title='mytitle')
            posts = Post.objects.search('mytitle')
            posts = [post for post in posts]

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].title, 'mytitle')

    def test_search_finds_term_in_body(self):
        with test_database(test_db, (Post,)):
            self.create_testdata(1, body='mybody')
            posts = Post.objects.search('mybody')
            posts = [post for post in posts]

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].body, 'mybody')

    def test_search_posts_only_returns_three(self):
        with test_database(test_db, (Post,)):
            self.create_testdata(4, body='mybody')
            posts = Post.objects.search('mybody')
            posts = [post for post in posts]

        self.assertEqual(len(posts), 3)
        self.assertEqual(posts[0].body, 'mybody')

    def test_search_posts_ordered_according_to_how_many_terms(self):
        pass

    def test_pagination(self):
        pass

    def test_edit_post(self):
        pass

    def test_highlight_search_terms(self):
        pass


