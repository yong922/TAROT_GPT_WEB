from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp


class UserLoginForm(FlaskForm):
    id = StringField('Input ID', validators=[DataRequired()])
    pw = PasswordField('Input PW', validators=[DataRequired()])


class UserCreateForm(FlaskForm):
    id = StringField('Input ID', validators=[DataRequired(), Length(min=3, max=20)])
    pw = PasswordField('Input PW', validators=[
        DataRequired(), EqualTo('pw2', '비밀번호가 일치하지 않습니다')])
    pw2 = PasswordField('Confirm PW', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired(), Length(min=2, max=15)])