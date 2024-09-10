from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import DataRequired

class Register(FlaskForm):
    email=EmailField(name='email',validators=[DataRequired()])
    password=PasswordField(name='password',validators=[DataRequired()])
    cpassword=PasswordField(name='confirm', validators=[DataRequired()])

class Login(FlaskForm):
    email=EmailField(name='email', validators=[DataRequired()])
    password=PasswordField(name='password',validators=[DataRequired()])