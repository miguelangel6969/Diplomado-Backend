from flask import Blueprint

# Objeto bluePirnt para manejar rutas
routes = Blueprint('routes', __name__)

#Se importan cada uno de los archivos que que contienen los servicios
from .UsuariosRoute import *
from .TransaccionRoute import *
from .WalletRoute import *