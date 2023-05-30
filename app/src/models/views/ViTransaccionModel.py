from src.db import db
from src.models.ModelParent import ModelParent

from src.db import db
from src.models.ModelParent import ModelParent

#Esta clase se convierte en un modelo de base de datos SQLAlchemy completo 
# con todas las funcionalidades proporcionadas por SQLAlchemy, como la capacidad 
# de realizar consultas, realizar operaciones de guardado y eliminación, entre otras
class ViTransaccionModel(db.Model, ModelParent):
    __tablename__ = 'transaccion_bloques'

    id = db.Column('id_transaccion', db.Integer, db.Sequence(
        'seq_transaccion'), primary_key=True, autoincrement=True)
    idBloque = db.Column('id_bloque',db.Integer)
    has = db.Column(db.String)
    origen = db.Column(db.String)
    destino = db.Column(db.String)
    monto = db.Column(db.Integer)