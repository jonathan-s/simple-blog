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
        pass


class PostSearchView(BaseView):

    def provide_context(self):
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
