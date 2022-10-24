from wtforms import Form, StringField, PasswordField, validators


class RegistrationForm(Form):
    name = StringField('Nome Completo', [validators.Length(min=4, max=80)])
    cpf = StringField('CPF', [validators.Length(min=4, max=80)])
    username = StringField('Usuario', [validators.Length(min=4, max=80)])
    email = StringField(
        'Email', [validators.Length(min=6, max=80), validators.Email()])
    password = PasswordField('Nova Senha', [
        validators.DataRequired(),
        validators.EqualTo('password',
                           message='Senha e confirmação não são iguais')
    ])
    confirm = PasswordField('Digite sua senha novamente')


class LoginFormulario(Form):
    email = StringField(
        'Email', [validators.Length(min=6, max=80), validators.Email()])
    password = PasswordField('Digite Sua Senha', [validators.DataRequired()])
