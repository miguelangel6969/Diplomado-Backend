from flask import jsonify, request

from src.models.UsuariosModel import UsuariosModel
from src.utils import convert_input_to
from . import routes
from ..schemas.UsuariosScheme import UsuariosSchema


@routes.route('/usuarios/list', methods=['POST'])
def listUsuarios():
    schema = UsuariosSchema(many=True)
    return jsonify(schema.dump(UsuariosModel.list(request.get_json())))


@routes.route('/usuarios/<int:id>', methods=['GET'])
def getUsuarios(id: int):
    schema = UsuariosSchema()
    return jsonify(schema.dump(UsuariosModel.find_by_id(id)))


@routes.route('/usuarios/<int:id>', methods=['DELETE'])
def deleteUsuarios(id: int):
    object = UsuariosModel.find_by_id(id)
    object.delete()
    return jsonify({'message': 'deleted'}), 200


@routes.route('/usuarios', methods=['POST'])
@convert_input_to(UsuariosModel)
def updateUsuarios(usuarios):
    schema = UsuariosSchema()
    usuarios.save()
    return jsonify(schema.dump(usuarios))
   

