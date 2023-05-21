from werkzeug.security import safe_str_cmp
import hashlib

##from werkzeug.security import safe_str_cmp

from src.models.UsuariosModel import UsuariosModel


def authenticate_user(email: str, password: str):
    try:
        user = UsuariosModel.find_by_email(email)
        passw = generar_hash_sha256(password)
        if safe_str_cmp(user.password, passw):
            return user
        return None
    except Exception as error:
        ##current_app.logger.error(error)
        return None

def get_id_user(email: str):
    user = UsuariosModel.find_by_email(email)
    if user is None:
        return None
    return user.id


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