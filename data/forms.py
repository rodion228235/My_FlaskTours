from flask_wtf import FlaskForm
import wtforms


class SignUpForm(FlaskForm):
    first_name = wtforms.StringField("Bведiть iм'я")
    last_name = wtforms.StringField("Bвeдiть iм'я")
    email = wtforms.EmailField("Email", validators=[wtforms.validators.DataRequired(), wtforms.validators.Email()])
    password = wtforms.PasswordField("Пapoль", validators=[wtforms.validators.length(8)]) 
    submit = wtforms.SubmitField("Зареєструватиcь")


class LoginForm(FlaskForm):
    email = wtforms.EmailField("Email", validators=[wtforms.validators.DataRequired(), wtforms.validators.Email()]) 
    password = wtforms.PasswordField("Пapoль", validators=[wtforms.validators.length(8)]) 
    submit = wtforms.SubmitField("Увiйти")
