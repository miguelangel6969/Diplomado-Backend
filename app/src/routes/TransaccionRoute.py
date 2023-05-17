from flask import jsonify, request
from flask_jwt_extended import get_jwt_claims, jwt_required

from src.models.transaccion import TransaccionModel
from src.models.views.ViTransaccionModel import ViTransaccionModel
from src.models.transaccion import TransaccionModel
from src.models.bloque import BloqueModel
from src.utils import convert_input_to
from src.db import db
from . import routes
from ..schemas.transaccionScheme import TransaccionSchema
from src.schemas.ViTransaccionScheme import ViTransaccionSchema
from ..schemas.BloqueScheme import BloqueSchema
import hashlib

@routes.route('/transaccion', methods=['POST'])
@jwt_required
def Transaccion():
    schema = ViTransaccionSchema(many=True)
    transacciones = jsonify(schema.dump(ViTransaccionModel.list({})))
    requestData = request.get_json()
    hasInicial="000000000000000000000000000000000000000000000000000000000000"
    print("-->", transacciones.get_json())
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
        
        sql = "EXEC sp_crear_transaccion {},'{}','{}','{}',{};".format(idBloque, hasBloque,requestData['origen'],requestData['destino'],requestData['monto'])
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

        return jsonify({"creo funciono":0})
    else:
        sql = "EXEC sp_crear_transaccion {},'{}','{}','{}',{};".format(requestData['idBloque'], hasInicial,requestData['origen'],requestData['destino'],requestData['monto'])
        db.session.execute(sql)
        db.session.commit()
        return jsonify({"no se haga coger fastidio":0})
    
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