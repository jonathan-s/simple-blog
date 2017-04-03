import os
from subprocess import call

from flask import Flask
from flask import g

from models.models import db, Post
from views.screens import (PostView,
                           PostListView,
                           PostSearchView,
                           PostEditView,
                           PostCreateView,
                           IndexView)

app = Flask(__name__)
app.config.from_pyfile('settings/__init__.py')
app.config.from_pyfile('settings/{}.py'.format(
    os.environ.get('environment', 'development')), silent=True)


def init_db():
    """Initializes the database."""
    call(['rm', 'post.db'])
    db.connect()
    db.create_tables([Post], safe=True)
    for x in xrange(1, 11):
        Post.create(title='Post-{}'.format(x),
                    body='lorem ipsum lorem ipsum')


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


@app.cli.command('tests')
def testcases():
    """Calls the unittests."""
    call(['python', '-B', '-m', 'unittest', 'discover'])

@app.before_request
def connect_db():
    if not hasattr(g, 'db'):
        g.db = db
        g.db.connect()

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

routes = [
    ('/post/<int:id>', PostView.as_view('post_view', template_name='post.html')),
    ('/posts/<int:page>', PostListView.as_view('post_list', template_name='post_list.html')),
    ('/search', PostSearchView.as_view('post_search', template_name='post_search.html')),
    ('/post/create', PostCreateView.as_view('post_create', template_name='post_edit_create.html')),
    ('/post/edit/<int:id>', PostEditView.as_view('edit', template_name='post_edit_create.html')),
    ('/', IndexView.as_view('index', template_name='index.html'))
]

for url, view in routes:
    app.add_url_rule(url, view_func=view)


if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    app.run()
