from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

# se utiliza posteriormente para interactuar con la base de datos, realizar
# consultas y manipular objetos de modelo.
db = SQLAlchemy()

# se utiliza para definir modelos de base de datos utilizando el enfoque declarativ
Base = declarative_base()