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

    def create_testdata(self):
        for number in xrange(10):
            Post.create(name='account-{}'.format(number),
                           email='bogus@email.com',
                           balance=200)

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

    def test_search_posts_only_returns_three(self):
        pass

    def test_search_posts_ordered_according_to_how_many_terms(self):
        pass

    def test_pagination(self):
        pass

    def test_edit_post(self):
        pass

    def test_highlight_search_terms(self):
        pass


