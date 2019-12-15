from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FormField, SelectField, FieldList, DateField, \
    DateTimeField, HiddenField, BooleanField, TimeField
from wtforms.validators import DataRequired, NumberRange

'''
Veja mais na documentação do WTForms

https://wtforms.readthedocs.io/en/stable/
https://wtforms.readthedocs.io/en/stable/fields.html

Um outro pacote interessante para estudar:

https://wtforms-alchemy.readthedocs.io/en/latest/

'''


class LoginForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    password = PasswordField('Senha', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    submit = SubmitField('Entrar')


class AgendaForm(FlaskForm):
    desc = StringField('Descrição', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    status = SelectField(u'Status', choices=[('en', 'Ativada'), ('dis', 'Desativada')])
    submit = SubmitField('Registrar')


class RegisterForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    submit = SubmitField('Inscrever')
    idA = ""
    idE = ""
    idU = ""


class EventoForm(FlaskForm):
    desc = StringField('Descrição')
    date = DateField('Dia', format='%d/%m/%Y', validators=[DataRequired("Valor de data inválido")])
    inicio = TimeField('Início', format='%H:%M', validators=[DataRequired("Valor de horário inválido")])
    fim = TimeField('Fim', format='%H:%M', validators=[DataRequired("Valor de horário inválido")])
    vagas = IntegerField('Vagas', validators=[DataRequired("Valor numérico inválido"),
                                              NumberRange(min=0, message="Valor deve ser positivo")])
    submit = SubmitField('Registrar')
