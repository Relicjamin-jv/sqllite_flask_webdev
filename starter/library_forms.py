from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import InputRequired, Optional, Length

class AuthorForm(FlaskForm):
    firstName = StringField("First Name", validators=[InputRequired()])
    middleInitial = StringField("Middle Initial", validators=[InputRequired(), Length(max=1)])
    lastName = StringField("Last Name", validators=[InputRequired()])
    submit = SubmitField("Submit")

class BookForm(FlaskForm):    
    # You will need to update the value of choices after creating an instance 
    # of your form in your handler. This is noted in app.py as well.
    author = SelectField("Author: ", choices=[])
    # TODO: add fields with validators for title and year