import re

from flask import redirect, url_for, flash, request
from wtforms import Form
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired
from peewee import DoesNotExist

from views import BaseView
from models.models import Post, PostDatabaseError


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
        posts = Post.objects.paginate(page)
        context = {'posts': list(posts)}
        return context


class PostSearchView(BaseView):

    methods = ['GET', 'POST']

    def generate_term_context(self, index, matches, post):
        new_body = ''
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
        return new_body, post

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
                new_body, post = self.generate_term_context(index, matches, post)

                post.body = post.body[index:]
                index = post.body.find(term)
            new_body = new_body.replace(term, '<b>{}</b>'.format(term))
            post.body = new_body + ' ...'
        return posts

    def post(self):
        search_form = SearchForm()
        search_form.process(request.form)
        if search_form.validate():
            self.redirect = url_for('post_search', q=search_form.query.data)

    def provide_context(self):
        query = request.args.get('q')
        search_form = SearchForm()
        if query:
            posts = Post.objects.search(query)
            highlighted = self.highlight_search(posts, query)
        else:
            highlighted = None
        return {'posts': highlighted, 'form': search_form}




class SearchForm(Form):
    query = StringField()


class PostForm(Form):
    title = StringField()
    body = TextAreaField()


class PostCreateView(BaseView):
    methods = ['GET', 'POST']

    def provide_context(self):
        postform = PostForm()
        return {'form': postform}

    def post(self):
        postform = PostForm()
        postform.process(request.form)
        if postform.validate():
            try:
                post = (Post
                        .objects
                        .create(title=postform.title.data,
                                body=postform.body.data))
                self.redirect = url_for('post_view', id=post.id)
            except PostDatabaseError as exc:
                return {'error': exc.message, 'form': postform}


class PostEditView(BaseView):
    methods = ['GET', 'POST']

    def provide_context(self):
        _id = self.parameters.get('id')
        postform = PostForm()
        if _id:
            post = Post.objects.get(_id)
            postform.title.data = post.title
            postform.body.data = post.body

        return {'form': postform, '_id': _id}

    def post(self):
        _id = self.parameters.get('id')
        postform = PostForm()
        postform.process(request.form)
        if postform.validate():
            try:
                _id = (Post
                        .objects
                        .edit(_id=_id,
                              title=postform.title.data,
                              body=postform.body.data))
                self.redirect = url_for('post_view', id=_id)
            except PostDatabaseError as exc:
                return {'error': exc.message, 'form': postform}


class IndexView(BaseView):

    def provide_context(self):
        return {}
