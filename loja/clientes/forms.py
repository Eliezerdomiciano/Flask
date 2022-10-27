from wtforms import Form, SubmitField, IntegerField, StringField, FloatField, TextAreaField, validators
from flask_wtf.file import FileAllowed, FileField, FileRequired


class Addprodutos(Form):
    name = StringField('Nome do Produto: ', [validators.DataRequired()])
    preco = FloatField('Preço do Produto: ', [validators.DataRequired()])
    desconto = IntegerField('Desconto do Produto: ', [validators.DataRequired()])
    estoque = IntegerField('Estoque do Produto: ', [validators.DataRequired()])
    descricao = StringField('Descrição do Produto: ', [validators.DataRequired()])
    cores = TextAreaField('Cor do Produto: ', [validators.DataRequired()])

    imagem_1 = FileField('Imagem 1: ', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    imagem_2 = FileField('Imagem 2: ', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    imagem_3 = FileField('Imagem 3: ', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])