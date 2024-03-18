from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
    )

    email = StringField(
        'E-mail',
        validators=[InputRequired(), Email(), Length(max=50)],
    )

    first_name = StringField(
        'First Name',
        validators=[InputRequired(), Length(min=2, max=50)],
    )

    last_name = StringField(
        'Last Name',
        validators=[InputRequired(), Length(min=2, max=50)],
    )

    password = PasswordField(
        'Password (6 characters minimum)',
        validators=[InputRequired(), Length(min=6, max=50)],
    )

    image_url = SelectField(
        'Profile Image',
        choices=[('/static/images/cobra.png', 'Select from the options: Cobra'),
                                  ('/static/images/monkey.png', 'Select from the options: Monkey'),
                                  ('/static/images/parrot.png', 'Select from the options: Falcon')],
        validators=[Length(max=255), InputRequired()]
    )


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        'Username',
        validators=[InputRequired(), Length(max=30)],
    )

    password = PasswordField(
        'Password',
        validators=[InputRequired(), Length(min=6, max=50)],
    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection."""


class ForgotPasswordForm(FlaskForm):
    """Form for retrieving lost password."""

    email = StringField('Email', validators=[InputRequired()])


class NewPasswordForm(FlaskForm):
    """Form for inputting new password."""

    password = PasswordField(
        'Password (6 characters minimum)',
        validators=[InputRequired(), Length(min=6, max=50)],
    )




