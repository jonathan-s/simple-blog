from wtforms import Form
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired

class SearchForm(Form):
    query = StringField()


class PostForm(Form):
    title = StringField()
    body = TextAreaField()
