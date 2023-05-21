from flask import Blueprint

routes = Blueprint('routes', __name__)

from .UsuariosRoute import *
from .TransaccionRoute import *
from .WalletRoute import *