from src.db import db
from src.models.ModelParent import ModelParent

from src.db import db
from src.models.ModelParent import ModelParent

class ViTransaccionModel(db.Model, ModelParent):
    __tablename__ = 'transaccion_bloques'

    id = db.Column('id_transaccion', db.Integer, db.Sequence(
        'seq_transaccion'), primary_key=True, autoincrement=True)
    idBloque = db.Column('id_bloque',db.Integer)
    has = db.Column(db.String)
    origen = db.Column(db.String)
    destino = db.Column(db.String)
    monto = db.Column(db.Integer)