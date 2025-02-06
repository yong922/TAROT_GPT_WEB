from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, ValidationError


class UserLoginForm(FlaskForm):
    id = StringField('Input ID', validators=[DataRequired()])
    pw = PasswordField('Input PW', validators=[DataRequired()])


def pw_complexity_check(form, field):
    pw = field.data
    digit = any(char.isdigit() for char in pw)
    alpha = any(char.isalpha() for char in pw)
    special = any(char in "!@#$%^&*()-_=+[{]}|;:'\",<.>/?`~" for char in pw)
    if not (digit and alpha and special):
        raise ValidationError('Password must include letters, numbers, and special characters.')

class UserCreateForm(FlaskForm):
    id = StringField('Input ID', 
        validators=[
            DataRequired(), 
            Length(min=3, max=20),
        ]
    )
    pw = PasswordField('Input PW', 
        validators=[
            DataRequired(), 
            Length(min=8, max=20),
            pw_complexity_check,
            EqualTo('pw2', 'The passwords do not match.')
        ]
    )
    pw2 = PasswordField('Confirm PW', validators=[DataRequired()])
    nickname = StringField('Nickname', 
        validators=[
            DataRequired(), 
            Length(min=2, max=15),
            Regexp('^[가-힣a-zA-Z0-9]+$', message='사용할 수 없는 기호가 포함돼있습니다.')
        ]
    )