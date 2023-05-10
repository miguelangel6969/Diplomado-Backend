from sqlalchemy_filters import apply_filters, apply_sort

from src.db import db


class ModelParent:

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def list(cls, json: dict):
        filter_spec = []
        for item, value in json.items():
            filter_spec.append({'field': item, 'op': '==', 'value': value})

        filtered_query = apply_filters(cls.query, filter_spec)

        return filtered_query.all()

    @classmethod
    def list_by_orden(cls, json: dict):
        filter_spec = []
        for item, value in json.items():
            filter_spec.append({'field': item, 'op': '==', 'value': value})

        filtered_query = apply_filters(cls.query, filter_spec)
        filtered_query = apply_sort(filtered_query, [{'field': 'orden', 'direction': 'asc'}])
        return filtered_query.all()

    @classmethod
    def list_by_fecha(cls, json: dict):
        filter_spec = []
        for item, value in json.items():
            filter_spec.append({'field': item, 'op': '==', 'value': value})

        filtered_query = apply_filters(cls.query, filter_spec)
        filtered_query = apply_sort(filtered_query, [{'field': 'fecha', 'direction': 'asc'}])
        return filtered_query.all()
