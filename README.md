# Nombre del proyecto

Api Block Chain

Proyecto desarrollado para lograr desarrollar una aplicación con una arquitectura de aplicación distribuida o arquitectura de microservicios. Donde este corresponde al backend. Con el objetivo de generar transacción y poder ver los registros correspondientes.

# Requisitos previos

Para poder compilar localmente este proyecto debes tener previamente instalado python.

Primero clona el proyecto: `https://github.com/miguelangel6969/Diplomado-Backend.git`

Se recomienda crear un ambiente virtual de python:

`python -m venv nombre_del_ambiente`

Luego de tener el ambiente se deberan instalar las librerias las cuales se encuentran en el archivo de requerimientos el cual se encuentra en la ruta: `app/requirements.` Para ejecutar este se debera de poner el siguiente código:

`pip install -r requirements.txt`

Esto instalara todas las librerias las cuales necesita la aplicación. Si no se quiere crear un entorno virtual se deberan isntalar las librerias de igual forma.

# Estructura del proyecto

`/app:` Contiene el código fuente y demás carpetas del proyecto
 - `app.py:` Archivo principal proyecto. en el cual se hace la configuración del mismo y se ejecuta.
 - `security.py:` Contiene metodos para validar usuarios y así generar token JWT

`/app/src:` contiene distribución de carpetas para la distibución de código.
  - `../models:` Se crean archivos .py con clases para realizar operaciones de búsqueda, guardado y eliminación en modelos SQLAlchemy
  - `../routes:` Se crean archivos .py con la logica de los servicios a utilizar con sus respectivas rutas
  - `../routes:` Se crean archivos .py con clases que se utilizan para definir un esquema de serialización y deserialización para los modelos
  - `../settings:`  se definen varios atributos de la clase que representan diferentes variables de entorno obtenidas del archivo .env. Estas variables de entorno incluyen configuraciones relacionadas con tokens JWT, configuraciones de base de datos, configuraciones de SQLAlchemy, modo de depuración, clave secreta JWT y otros
  - `db.py:` Se utiliza posteriormente para interactuar con la base de datos, realizar consultas y manipular objetos de modelo.

# Despliegue mediante Docker

- Ubiquese en la ruta `/app`
- Verifique su conexión a internet
- Verifique tener instalado docker en Su maquina. En caso de se debera instalar
- corra el siguiente comando `docker compose up` esto se encargara de bajar las imagenes requeridas y de crear una red para estas. Una vez haya creado los debidos contenedores de las imagenes pondra a correr estos mismos y podra interactuar con la app.







