from src.ma import ma 
from src.models.transaccion import TransaccionModel

class TransaccionSchema(ma.SQLAlchemyAutoSchema): 
	 class Meta: 
 		model = TransaccionModel