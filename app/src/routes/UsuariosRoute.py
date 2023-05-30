from flask import jsonify, request
from flask_jwt_extended import get_jwt_claims, jwt_required
from src.models.UsuariosModel import UsuariosModel
from src.utils import convert_input_to
from . import routes
from ..schemas.UsuariosScheme import UsuariosSchema
import hashlib

#Obtener todos los usuarios del sistema
@routes.route('/usuarios/list', methods=['GET'])
def listUsuarios():
    schema = UsuariosSchema(many=True)
    return jsonify(schema.dump(UsuariosModel.list({})))

#obtener data de un usuario especifico
@routes.route('/usuario/data', methods=['GET'])
@jwt_required
def getUsuarios():
    schema = UsuariosSchema()
    claims = get_jwt_claims()
    user = claims['idUsuario']
    return jsonify(schema.dump(UsuariosModel.find_by_id(user)))

#creación usuarios
@routes.route('/usuarios', methods=['POST'])
@convert_input_to(UsuariosModel)
def updateUsuarios(usuarios):
    try:
        email = UsuariosModel.find_by_email(usuarios.email)
        indentification = UsuariosModel.find_by_cedula(usuarios.cedula)
        #se valida que los campos unicos no existan ya en la base de datos
        if email and indentification:
            return jsonify({"message":"Correo y cedula existentes"}), 400
        elif email:
            return jsonify({"message":"Correo existente"}), 400
        elif indentification:
            return jsonify({"message":"Cedula existente"}), 400
        else:
            schema = UsuariosSchema()
            usuarios.email = usuarios.email.strip()
            usuarios.cedula = usuarios.cedula.strip()
            key = generar_hash_sha256(usuarios.email+""+usuarios.cedula)
            usuarios.user_key=key
            usuarios.saldo = 0
            passw = generar_hash_sha256(usuarios.password)
            usuarios.password = passw
            usuarios.save()
            return jsonify({"message": "Usuario creado con éxito"})
    except Exception as error:
        ##current_app.logger.error(error)
        return jsonify({"message": "Error interno del servidor"}), 500

#Se Encripta la contraseña
def generar_hash_sha256(datos):
    # Crear un objeto hash SHA-256
    sha256_hash = hashlib.sha256()

    # Convertir los datos en una cadena de bytes antes de pasarlos al algoritmo de hash
    datos_bytes = datos.encode('utf-8')

    # Pasar los datos al objeto hash
    sha256_hash.update(datos_bytes)

    # Obtener el valor hash en formato hexadecimal
    hash_resultado = sha256_hash.hexdigest()

    # Devolver el hash generado
    return hash_resultado
   

