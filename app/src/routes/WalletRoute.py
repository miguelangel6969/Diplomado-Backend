from flask import jsonify, request
from flask_jwt_extended import get_jwt_claims, jwt_required

from src.models.UsuariosModel import UsuariosModel
from src.utils import convert_input_to
from . import routes
from ..schemas.UsuariosScheme import UsuariosModel

#Obtener saldo al usuario que se encuentra en sesión
@routes.route('/wallet/saldo', methods=['GET'])
@jwt_required
def GetSaldo():
    try:
        claims = get_jwt_claims()
        user = claims['idUsuario']
        wallet = UsuariosModel.find_by_id(user)
        if wallet:
            return jsonify({"saldo": wallet.saldo})
        return jsonify({"message": "No se encontro saldo para este usuario"}), 400
    except Exception as error:
        ##current_app.logger.error(error)
        return jsonify({"message": "Error interno del servidor"}), 500

#Dar saldo a un usuario
@routes.route('/wallet/saldo', methods=['POST'])
@jwt_required
def Saldo():
    try:
        requestData = request.get_json()
        e = UsuariosModel.find_by_id(requestData['idUsuario'])
        e.id = requestData['idUsuario']
        e.saldo = e.saldo+requestData['saldo']
        e.save()
        return jsonify({"message": "Saldo editado con exito"})
    except Exception as error:
        ##current_app.logger.error(error)
        return jsonify({"message": "Error interno del servidor"}), 500