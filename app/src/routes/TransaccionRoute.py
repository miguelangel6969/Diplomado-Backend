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

@routes.route('/transaccion', methods=['POST'])
@jwt_required
def Transaccion():
    schema = ViTransaccionSchema(many=True)
    requestData = request.get_json()
    claims = get_jwt_claims()
    user = claims['idUsuario']
    usuario = UsuariosModel.find_by_id(user)
    tran = True
    if usuario:
        if usuario.saldo is not None:
            if usuario.saldo < requestData['monto']:
                tran = False
        else:
             tran= False
    else:
         tran=False
    
    if tran==False:
         return jsonify({"message":"El monto del usuario no cubre la transacción"}), 400
    
    transacciones = jsonify(schema.dump(ViTransaccionModel.list({})))
    hasInicial="000000000000000000000000000000000000000000000000000000000000"
    if(len(transacciones.get_json())>0):
        bloque=transacciones.get_json()
        idBloque=bloque[len(bloque) - 1]["idBloque"]
        contBloq = 0
        hasBloque=''
        for i in bloque:
            if i["idBloque"]==idBloque:
                contBloq+=1

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
        if count>=2:
            transaccion = TransaccionModel.find_by_transaccion(idBloque)
            nuevoHas=crearNuevoHash(transaccion,listTran)
            b = BloqueModel.find_by_id(idBloque)
            b.id = idBloque
            b.has = nuevoHas
            b.save()        

        return jsonify({"message":"Transacción exitosa"})
    else:
        sql = "EXEC sp_crear_transaccion {},'{}','{}','{}',{};".format(requestData['idBloque'], hasInicial,usuario.user_key,requestData['destino'],requestData['monto'])
        print("--> ",sql)
        db.session.execute(sql)
        db.session.commit()
        return jsonify({"message":"Transacción exitosa"})
    
@routes.route('/transaccion/historial', methods=['GET'])
@jwt_required
def Historial():
     
     claims = get_jwt_claims()
     user = claims['idUsuario']

     usuario = UsuariosModel.find_by_id(user)

     if usuario:
        print("--> ",usuario.user_key)
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

        print("sql---> ",sql)
        resultados = db.session.execute(sql, {"origen": usuario.user_key, "destino": usuario.user_key})
        print("ejecucion-- ",resultados)
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
        m.update(repr(trans).encode())
        hashInvalido = m.hexdigest()
        hashValido = comprobarHash(hashInvalido, listTrans)
        return hashValido

def comprobarHash(hashInvalido, listTrans):
        invalido = hashInvalido
        valor = 0
        aceptado = False
        
        while aceptado == False:
            while invalido[0:4] != "0000":
                invalido = modHash(invalido, valor)
                valor += 1
            
            if len(listTrans) == 1:
                aceptado = True
            else:
                nuevoV = True
                for codigo in listTrans:
                    if invalido[0:4] == "0000" and codigo == invalido:
                        nuevoV = False
                        invalido = modHash(invalido, valor)
                        valor += 1
                    elif invalido[0:4] != "0000":
                        nuevoV = False

                if nuevoV == True:
                    aceptado = True 

        return invalido

def modHash(invalido, valor):
        m = hashlib.sha256()
        hashNuevo = invalido + str(valor)
        m.update(hashNuevo.encode())
        invalido = m.hexdigest()
        return invalido
