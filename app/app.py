import json
import logging
import time
from datetime import date
from http.client import HTTPConnection, HTTPResponse, HTTPSConnection

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager,jwt_required, create_access_token, create_refresh_token, jwt_refresh_token_required, \
    get_jwt_identity
from flask_restful import Api

from security import authenticate_user, get_id_user
from src.db import db
from src.doc import docs
from src.ma import ma

from src.routes import *
from src.settings.settings import Settings

app = Flask(__name__)
# configuracion de app
app.config.from_object(Settings())

# CORS
CORS(app)
api = Api(app=app)
jwt = JWTManager(app=app)

#Token expirado
@jwt.expired_token_loader
def custom_expired_token_loader_callback():
    return jsonify({'message': 'Tu sesion ha caducado'}), 401


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return jsonify(ret), 404


@app.route('/')
def hello_world():
    return 'Api is running'

#Autenticación
@app.route('/auth', methods=['POST'])
def login():
    user_json = request.get_json()
    try:
        #Se valida el correo y la contraseña
        user = authenticate_user(user_json['email'], user_json['password'])
        email = user.email
        #se crea token
        access_token = create_access_token(email)
        #se crea llave para refrescar token
        refresh_token = create_refresh_token(user.email)
        return jsonify({"access_token": access_token, "refresh_token": refresh_token})
    except Exception as e:
        ##app.logger.error(e)
        return jsonify({"message": "El usuario no existe."}), 404

#Se guardan variables en el token
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'identity': identity,
        'idUsuario': get_id_user(identity)
    }


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@app.route('/protected', methods=['POST'])
@jwt_required
def get_additional_data_user():
    claims = get_jwt_claims()
    return jsonify(claims), 200

#Se registran las rutas que contenga el objeto blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    app.logger.info('configuracion incial=> {}'.format(app.config))
    db.init_app(app=app)
    ma.init_app(app=app)
    docs.init_app(app=app)
    app.run(host='0.0.0.0', port=5000)
