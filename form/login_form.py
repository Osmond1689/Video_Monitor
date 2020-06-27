from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField 
from wtforms.validators import DataRequired 
   
   
class LoginForm(FlaskForm): 
    accountNumber = StringField('',validators=[DataRequired('accountNumber is null')]) 
    password = PasswordField( '',validators=[DataRequired('password is null')]) 
