from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import InputRequired, Email, EqualTo
from flask_wtf.file import FileAllowed, FileRequired

class SignUpForm(FlaskForm):
    full_name = StringField('Full Name', validators = [InputRequired()])
    email = StringField('Email',
                        validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators = [InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit = SubmitField('Login')

class createPlantForm(FlaskForm):
    name = StringField("Plant Name", validators=[InputRequired()])
    type = StringField("Plant Type", validators = [InputRequired()])
    bio = TextAreaField("Bio", validators = [InputRequired()])
    image = FileField("Plant Image", validators=[FileRequired(), FileAllowed(["jpg","jpeg","png"], "Images only!")])
    submit = SubmitField("Create Plant")

class EditPlantForm(FlaskForm):
    name = StringField("Plant Name", validators = [InputRequired()])
    type = StringField("Plant Type", validators = [InputRequired()])
    bio = TextAreaField("Plant Bio", validators = [InputRequired()])
    submit = SubmitField("Save Edits")