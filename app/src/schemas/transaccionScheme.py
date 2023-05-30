from src.ma import ma 
from src.models.transaccion import TransaccionModel

#Esta clase se utiliza para definir un esquema de serialización y deserialización para el modelo
class TransaccionSchema(ma.SQLAlchemyAutoSchema): 
	 class Meta: 
 		model = TransaccionModel