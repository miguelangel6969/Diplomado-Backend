from src.db import db
from src.models.ModelParent import ModelParent

#Esta clase se convierte en un modelo de base de datos SQLAlchemy completo 
# con todas las funcionalidades proporcionadas por SQLAlchemy, como la capacidad 
# de realizar consultas, realizar operaciones de guardado y eliminación, entre otras
class BloqueModel(db.Model, ModelParent):
    __tablename__ = 'bloque'

    id = db.Column('id_bloque', db.Integer, db.Sequence(
        'seq_bloque'), primary_key=True, autoincrement=True)
    has = db.Column(db.String)


