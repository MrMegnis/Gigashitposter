from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class VkTokenForm(FlaskForm):
    token = StringField('Токен сюда:', validators=[DataRequired()])
    submit = SubmitField('Отдать')
