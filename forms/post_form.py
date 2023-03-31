from flask_wtf import FlaskForm
from wtforms import StringField, MultipleFileField, DateTimeLocalField, SubmitField, TimeField
from wtforms.validators import DataRequired
import datetime


class PostForm(FlaskForm):
    id = StringField('Id сообщества', validators=[DataRequired()])
    tag = StringField('Теги на Deviantart(через запятую)')
    images = MultipleFileField('Картинки(Если не указаны теги)')
    start_on = DateTimeLocalField('Начиная с:', format="%Y-%m-%dT%H:%M", default=datetime.datetime.now())
    interval = TimeField('Интервал:', default=datetime.time(0))
    submit = SubmitField('Продолжить')
