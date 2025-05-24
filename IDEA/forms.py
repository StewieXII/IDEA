from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class RegistroForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    contraseña = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class CheckoutForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[DataRequired()])
    direccion_envio = StringField('Dirección de envío', validators=[DataRequired()])
    metodo_pago = SelectField('Método de pago', choices=[('tarjeta', 'Tarjeta'), ('contrareembolso', 'Contrareembolso')])
    submit = SubmitField('Confirmar pedido')
