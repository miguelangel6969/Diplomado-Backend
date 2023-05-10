from flask import current_app

##from werkzeug.security import safe_str_cmp

from src.models.UsuariosModel import UsuariosModel


def authenticate_user(user: str, password: str):
    try:
        user = UsuariosModel.find_by_user(user)
        if user:
            return user
        return None
    except Exception as error:
        ##current_app.logger.error(error)
        return None

def get_id_user(email: str):
    user = UsuariosModel.find_by_user(email)
    if user is None:
        return None
    return user.id
