from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required
#表单类
class NameForm(FlaskForm):
    name=StringField("what is your name?",validators=[Required()])
    submit=SubmitField("submit")