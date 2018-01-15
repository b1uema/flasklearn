from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextField,BooleanField,SelectField,SubmitField
from wtforms.validators import Required
from ..models import Role,User
from wtforms import ValidationError
#表单类
class NameForm(FlaskForm):
    name=StringField("what is your name?",validators=[Required()])
    submit=SubmitField("submit")


class EditProfileForm(FlaskForm):
    name = StringField('Real name',validators=[Length(0,64)])