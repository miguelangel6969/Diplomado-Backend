from src.ma import ma 
from src.models.UsuariosModel import UsuariosModel

class UsuariosSchema(ma.SQLAlchemyAutoSchema): 
	 class Meta: 
 		model = UsuariosModel
