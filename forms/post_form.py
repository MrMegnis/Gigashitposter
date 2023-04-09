from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, DateTimeLocalField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired
import datetime


class PostForm(FlaskForm):
    # id = StringField('Id сообщества', validators=[DataRequired()])param[0]
    id = SelectField('Id сообщества', coerce=int)
    tag = StringField('Тег на Deviantart')
    images = MultipleFileField('Картинки')
    start_on = DateTimeLocalField('Начиная с:', format="%Y-%m-%dT%H:%M", default=datetime.datetime.now())
    interval = TimeField('Интервал:', default=datetime.time(0))
    submit = SubmitField('Продолжить')
