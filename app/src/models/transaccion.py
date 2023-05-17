from src.db import db
from src.models.ModelParent import ModelParent

class TransaccionModel(db.Model, ModelParent):
    __tablename__ = 'transaccion'

    id = db.Column('id_transaccion', db.Integer, db.Sequence(
        'seq_transaccion'), primary_key=True, autoincrement=True)
    idBloque = monto = db.Column('id_bloque',db.Integer)
    origen = db.Column(db.String)
    destino = db.Column(db.String)
    monto = db.Column(db.Integer)

    @classmethod
    def find_by_transaccion(cls, _idbloque):
        return cls.query.filter_by(idBloque=_idbloque).first()