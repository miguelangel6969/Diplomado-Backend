from sqlalchemy_filters import apply_filters, apply_sort

from src.db import db

#Esta clase proporciona métodos comunes 
# para realizar operaciones de búsqueda, guardado y eliminación en modelos SQLAlchemy
class ModelParent:

    #realiza una consulta en la base de datos para buscar un registro por su identificador único
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    #realiza una consulta para obtener todos los
    #registros del modelo. Retorna una lista con todos los registros
    @classmethod
    def find_all(cls):
        return cls.query.all()

    # guarda el objeto actual en la base de datos. Agrega el objeto a la sesión de base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()

    #elimina el objeto actual de la base de dato
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    #realiza una consulta filtrada en base a un diccionario de filtros 
    @classmethod
    def list(cls, json: dict):
        filter_spec = []
        for item, value in json.items():
            filter_spec.append({'field': item, 'op': '==', 'value': value})

        filtered_query = apply_filters(cls.query, filter_spec)

        return filtered_query.all()

    #ordena los resultados por el campo "orden" en orden ascendente
    @classmethod
    def list_by_orden(cls, json: dict):
        filter_spec = []
        for item, value in json.items():
            filter_spec.append({'field': item, 'op': '==', 'value': value})

        filtered_query = apply_filters(cls.query, filter_spec)
        filtered_query = apply_sort(filtered_query, [{'field': 'orden', 'direction': 'asc'}])
        return filtered_query.all()

    #ordena los resultados por el campo "fecha" en orden ascendente
    @classmethod
    def list_by_fecha(cls, json: dict):
        filter_spec = []
        for item, value in json.items():
            filter_spec.append({'field': item, 'op': '==', 'value': value})

        filtered_query = apply_filters(cls.query, filter_spec)
        filtered_query = apply_sort(filtered_query, [{'field': 'fecha', 'direction': 'asc'}])
        return filtered_query.all()
