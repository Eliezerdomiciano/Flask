from loja import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(240), unique=False, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    username = db.Column(db.String(180), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    perfil = db.Column(db.String(180), unique=False,
                       nullable=False, default='perfil.jpg')

    def __repr__(self):
        return '<User %r>' % self.username


db.create_all()
