import unittest

from playhouse.test_utils import test_database
from peewee import SqliteDatabase
from mock import MagicMock

from models.models import Post

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

