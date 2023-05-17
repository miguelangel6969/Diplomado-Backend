from src.db import db
from src.models.ModelParent import ModelParent

class UsuariosModel(db.Model, ModelParent):
    __tablename__ = 'usuarios'

    id = db.Column('id_user', db.Integer, db.Sequence(
        'seq_usuarios'), primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    usuario = db.Column(db.String)
    password = db.Column(db.String)
    nombres = db.Column(db.String)
    apellidos = db.Column(db.String)
    cedula = db.Column(db.String)
    user_key = db.Column(db.String)

    @classmethod
    def find_by_user(cls, _user):
        return cls.query.filter_by(usuario=_user).first()

