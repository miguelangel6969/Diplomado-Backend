from src.ma import ma 
from src.models.bloque import BloqueModel

#Esta clase se utiliza para definir un esquema de serialización y deserialización para el modelo
class BloqueSchema(ma.SQLAlchemyAutoSchema): 
	 class Meta: 
 		model = BloqueModel