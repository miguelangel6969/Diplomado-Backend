from src.models.views.ViTransaccionModel import ViTransaccionModel
from src.ma import ma

#Esta clase se utiliza para definir un esquema de serialización y deserialización para el modelo
class ViTransaccionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ViTransaccionModel