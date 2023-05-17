from src.ma import ma 
from src.models.bloque import BloqueModel

class BloqueSchema(ma.SQLAlchemyAutoSchema): 
	 class Meta: 
 		model = BloqueModel