from flask import jsonify, request
from flask_jwt_extended import get_jwt_claims, jwt_required

from src.models.transaccion import TransaccionModel
from src.models.views.ViTransaccionModel import ViTransaccionModel
from src.models.transaccion import TransaccionModel
from src.models.bloque import BloqueModel
from src.models.UsuariosModel import UsuariosModel
from src.utils import convert_input_to
from src.db import db
from . import routes
from src.schemas.ViTransaccionScheme import ViTransaccionSchema
import hashlib
from sqlalchemy import text

#Realizar transacción en bloque
@routes.route('/transaccion', methods=['POST'])
@jwt_required
def Transaccion():
    schema = ViTransaccionSchema(many=True) #Se obtienen el esquema de la tabla transacción
    requestData = request.get_json() # se recupera la data enviada en el cuerpo de la petición
    claims = get_jwt_claims() # se guardan los claims (variables del token)
    user = claims['idUsuario'] # se recupera el id del usuario por el claim
    usuario = UsuariosModel.find_by_id(user) # se busca la información del usuario
    tran = True
    if usuario: # si el usuario existe
        if usuario.saldo is not None: # se valida que tenga saldo
            if usuario.saldo < requestData['monto']: # se valida que el saldo de la transacción no supere el saldo
                tran = False
        else:
             tran= False
    else:
         tran=False
    
    if tran==False: # se la variable llega en false, no se puede hacer la transacción
         return jsonify({"message":"El monto del usuario no cubre la transacción"}), 400
    
    transacciones = jsonify(schema.dump(ViTransaccionModel.list({}))) # Se obtienen las transacciones
    hasInicial="000000000000000000000000000000000000000000000000000000000000" # HASH Inicial
    if(len(transacciones.get_json())>0): 
        bloque=transacciones.get_json() #Se convierte en json las transacciones obtenidodas
        idBloque=bloque[len(bloque) - 1]["idBloque"] # se obtiene la ultima posición para obtener el ultimo bloque
        contBloq = 0
        hasBloque=''
        for i in bloque:
            if i["idBloque"]==idBloque:
                contBloq+=1 #contador de cuantas veces se encuentra el bloque seleccionado

        if contBloq>2: 
             idBloque=0
             hasBloque=hasInicial
        
        sql = "EXEC sp_crear_transaccion {},'{}','{}','{}',{};".format(idBloque, hasBloque,usuario.user_key,requestData['destino'],requestData['monto'])
        db.session.execute(sql)
        db.session.commit()

        count=0
        listTran=[]
        for i in transacciones.get_json():
            if i["has"] not in listTran :
                listTran.append(i["has"])

            if i["idBloque"]==idBloque:
                count+=1
         # si el bloque se encuentra dos veces significa que va a hacer su tercera transacción
        # así que se debe cerrar el bloque
        if count>=2:
            transaccion = TransaccionModel.find_by_transaccion(idBloque)
            nuevoHas=crearNuevoHash(transaccion,listTran) # se recupera nuevo hash
            b = BloqueModel.find_by_id(idBloque)
            b.id = idBloque
            b.has = nuevoHas
            b.save() # se actualiza el bloque     

        return jsonify({"message":"Transacción exitosa"})
    else:
        sql = "EXEC sp_crear_transaccion {},'{}','{}','{}',{};".format(requestData['idBloque'], hasInicial,usuario.user_key,requestData['destino'],requestData['monto'])
        print("--> ",sql)
        db.session.execute(sql)
        db.session.commit()
        return jsonify({"message":"Transacción exitosa"})

#Obtener historial transacciones realizadas por un usuario
@routes.route('/transaccion/historial', methods=['GET'])
@jwt_required
def Historial():
     
     claims = get_jwt_claims() #se recuperan variables del token
     user = claims['idUsuario'] # se obtiene el id del usuario

     usuario = UsuariosModel.find_by_id(user) # se obtiene la data del usuario

     if usuario:
        sql = text(
            "SELECT T1.id_transaccion, T1.id_bloque, U3.nombres AS nombre_origen, T1.fecha, U2.nombres AS nombre_destino, T1.monto, 'Saliente' as tipo "
            "FROM transaccion T1 "
            "JOIN usuarios U2 ON T1.destino = U2.user_key "
            "JOIN usuarios U3 ON T1.origen = U3.user_key "
            "WHERE T1.origen = :origen "
            "UNION ALL "
            "SELECT T1.id_transaccion, T1.id_bloque, U3.nombres AS nombre_origen, T1.fecha, U2.nombres AS nombre_destino, T1.monto, 'Entrante' as tipo "
            "FROM transaccion T1 "
            "JOIN usuarios U2 ON T1.destino = U2.user_key "
            "JOIN usuarios U3 ON T1.origen = U3.user_key "
            "WHERE T1.destino = :destino"
        )

        resultados = db.session.execute(sql, {"origen": usuario.user_key, "destino": usuario.user_key})
        response = []
        for fila in resultados:
             if fila.tipo == 'Entrante':
                  response.append( { 'monto': fila.monto, "usuario": fila.nombre_origen, "fecha": fila.fecha, "positivo":True } )
             else:
                  response.append( { 'monto': fila.monto, "usuario": fila.nombre_destino, "fecha": fila.fecha, "positivo":False } )
        

        return jsonify(response)
     else:
          return jsonify({"message":"No se encontro el usuario"}) , 400

    
def crearNuevoHash(trans, listTrans):
        m = hashlib.sha256()
        m.update(repr(trans).encode()) #se vuelve string los bloques
        hashInvalido = m.hexdigest() #se valida que el hash sea valido
        hashValido = comprobarHash(hashInvalido, listTrans) # se hace prueba de trabajo
        return hashValido

def comprobarHash(hashInvalido, listTrans):
        invalido = hashInvalido
        valor = 0
        aceptado = False
        
        while aceptado == False:
            while invalido[0:4] != "0000": # El hash debe tener sus primeros 4 caracteres en 0
                invalido = modHash(invalido, valor) #se genera hash
                valor += 1 #se aumenta auxiliar
            
            #si las transacciones tienen una significa que el hash es el primero entonces 
            #no se reliza comparaciones
            if len(listTrans) == 1: 
                aceptado = True
            else:
                nuevoV = True
                for codigo in listTrans:
                    #Si el hash ya existe se genera otro de lo contrario se retorna
                    if invalido[0:4] == "0000" and codigo == invalido:
                        nuevoV = False
                        invalido = modHash(invalido, valor)
                        valor += 1
                    #el hash si o si debe tener sus 4 caracteres en 0
                    elif invalido[0:4] != "0000":
                        nuevoV = False

                if nuevoV == True:
                    aceptado = True 

        return invalido

#se genera hash concatenando el auxiliar para que siempre genere un hash nuevo
def modHash(invalido, valor):
        m = hashlib.sha256()
        hashNuevo = invalido + str(valor)
        m.update(hashNuevo.encode())
        invalido = m.hexdigest()
        return invalido
