from flask_wtf import FlaskForm
import wtforms


class SignUP(FlaskForm):
    first_name = wtforms.StringField("Введіть ім'я")
    last_name = wtforms.StringField("Введіть призвіще")
    email = wtforms.EmailField("Email", validators=[wtforms.validators.Email()])
    password = wtforms.PasswordField("Введіть пароль", validators=[wtforms.validators.length(8)])
    
    
class LoginForm(FlaskForm):
    email = wtforms.EmailField("Email", validators=[wtforms.validators.DataRequired(), wtforms.validators 