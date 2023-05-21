from src.db import db
from src.models.ModelParent import ModelParent

class UsuariosModel(db.Model, ModelParent):
    __tablename__ = 'usuarios'

    id = db.Column('id_user', db.Integer, db.Sequence(
        'seq_usuarios'), primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    nombres = db.Column(db.String)
    apellidos = db.Column(db.String)
    cedula = db.Column(db.String)
    user_key = db.Column(db.String)
    saldo = db.Column(db.Integer)

    @classmethod
    def find_by_email(cls, _email):
        return cls.query.filter_by(email=_email).first()
    
    @classmethod
    def find_by_cedula(cls, _ced):
        return cls.query.filter_by(cedula=_ced).first()
    
    @classmethod
    def find_by_key(cls, _key):
        return cls.query.filter_by(user_key=_key).first()

