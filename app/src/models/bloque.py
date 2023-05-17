from src.db import db
from src.models.ModelParent import ModelParent

class BloqueModel(db.Model, ModelParent):
    __tablename__ = 'bloque'

    id = db.Column('id_bloque', db.Integer, db.Sequence(
        'seq_bloque'), primary_key=True, autoincrement=True)
    has = db.Column(db.String)


