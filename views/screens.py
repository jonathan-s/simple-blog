import re

from flask import redirect, url_for, flash, request
from wtforms import Form
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired
from peewee import DoesNotExist

from views import BaseView
from models.models import Post


class PostView(BaseView):

    def provide_context(self):
        try:
            _id = self.parameters.get('id')
            post = Post.objects.get(_id)
            context = {'post': post}
        except DoesNotExist:
            context = {'status': 404}
        return context


class PostListView(BaseView):

    def provide_context(self):
        page = self.parameters.get('page')
        posts = Post.objects.paginate(2)
        context = {'posts': list(posts)}
        return context


class PostSearchView(BaseView):

    def highlight_search(self, posts, term):
        for post in posts:
            index = 0
            new_body = ''
            index = 0
            while index != -1:
                index = post.body.find(term)
                if index == 0:
                    index = post.body[1:].find(term)
                    continue
                matches = re.finditer(r'\w+', post.body)

                temp_matches = []
                for no, m in enumerate(matches):
                    if m.start() >= index:
                        if len(temp_matches) < 2:
                            start_len = len(temp_matches)
                        else:
                            start_len = 2
                        start_context = temp_matches[no - start_len].start()

                        try:
                            amount_matches = len(temp_matches)
                            temp_matches.append(matches.next())
                            temp_matches.append(matches.next())
                        except StopIteration:
                            pass
                        finally:
                            end_context = temp_matches[-1].end()
                            new_body = new_body + '... ' + post.body[start_context:end_context]

                    temp_matches.append(m)
                post.body = post.body[index:]
                index = post.body.find(term)
            new_body = new_body.replace(term, '<b>{}</b>'.format(term))
            post.body = new_body + ' ...'
        return posts

    def provide_context(self):
        query = request.args.get('q')
        posts = Post.objects.search(query)
        highlighted = self.highlight_search(posts, query)
        return {'posts': highlighted}


class SearchForm(Form):
    pass


class PostForm(Form):
    pass


class PostCreateEditView(BaseView):
    methods = ['GET', 'POST', 'PUT']

    def provide_context(self):
        pass

    def post(self):
        postform = PostForm()
        postform.process(request.form)
        if postform.validate():
            pass


class IndexView(BaseView):

    def provide_context(self):
        return {}
