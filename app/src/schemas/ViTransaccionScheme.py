from src.models.views.ViTransaccionModel import ViTransaccionModel
from src.ma import ma


class ViTransaccionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ViTransaccionModel