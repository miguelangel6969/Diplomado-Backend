from src.ma import ma 
from src.models.UsuariosModel import UsuariosModel

#Esta clase se utiliza para definir un esquema de serialización y deserialización para el modelo
class UsuariosSchema(ma.SQLAlchemyAutoSchema): 
	 class Meta: 
 		model = UsuariosModel
