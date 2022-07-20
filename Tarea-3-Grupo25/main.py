from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta

import jsonschema
from config import config
from models import db, Reproducciones, Personas, Canciones, Facturas


def create_app(enviroment):
	app = Flask(__name__)
	app.config['JSON_AS_ASCII'] = False
	app.config.from_object(enviroment)
	with app.app_context():
		db.init_app(app)
		db.create_all()
	return app


# Accedemos a la clase config del archivo config.py
enviroment = config['development']
app = create_app(enviroment)
app.config['JSON_SORT_KEYS'] = False
CORS(app)


#===============================================================================#
#CRUD PERSONAS
#===============================================================================#
#READ PERSONA
@app.route('/api/persona/<id>', methods=['GET'])
def get_persona(id):
    persona = Personas.query.filter_by(id=id).first()
    if persona:
        response = jsonify(persona.json())
        return response
    else:
        return 'Persona no existe', 404

#CREATE PERSONA
@app.route('/api/persona', methods=['POST'])
def put_persona():
    body = request.get_json()
    persona = Personas()
    mensaje = 'Campos nombre, email, password y tipo_persona son obligatorios.'

    #Se asume que al crear una persona se envían todas las keys, por lo tanto no se revisa si la key existe, solo si es que null
    if body.get('nombre') is not None and body.get('email') is not None and body.get('password') is not None and body.get('tipo_de_persona') is not None:
        if body.get('nombre').replace(" ","") != '' and body.get('email').replace(" ", "") != '' and body.get('password').replace(" ", "") != '':
            persona.nombre = body['nombre']
            persona.email = body['email']
            persona.password = body['password']
            persona.tipo_de_persona = body['tipo_de_persona']
        else: 
            return mensaje, 400
    else:
        return mensaje, 400

    #Se asigna el resto
    persona.apellido = body['apellido']
    persona.usuario_suscripcion = body['usuario_suscripcion']
    persona.artista_nombre_artistico = body['artista_nombre_artistico']
    persona.artista_verificado = body['artista_verificado']
    persona = Personas.create(persona)   #se crea persona
    response = jsonify(persona.json())
    return response, 201
    

#UPDATE PERSONA
@app.route('/api/persona/<id>', methods=['PUT'])
def edit_persona(id):
    body = request.get_json()
    persona = Personas.query.filter_by(id=id).first()    #Datos actuales de persona
    if not persona:
        return 'Persona no existe.', 404
    error = 'Campos nombre, email, password y tipo_persona son obligatorios.'

    #Si es que el atributo es NULL, se revisa si es porque la key no viene o porque es NULL
    #Luego se revisa si vienen vacios ej: "", "    " 
    if body.get('nombre') is None:
        if 'nombre' in body:
            return error, 400
    else:
        if body.get('nombre').replace(" ", "") == '':
            return error, 400
        else:
            persona.nombre = body['nombre']

    if body.get('email') is None:
        if 'email' in body:
            return error, 400
    else:
        if body.get('email').replace(" ", "") == '':
            return error, 400
        else:
            persona.email = body['email']

    if body.get('password') is None:
        if 'password' in body:
            return error, 400
    else:
        if body.get('password').replace(" ", "") == '':
            return error, 400
        else:
            persona.password = body['password']

    if body.get('tipo_de_persona') is None:
        if 'tipo_de_persona' in body:
            return error, 400
    else:
        persona.tipo_de_persona = body['tipo_de_persona']

    #Resto de los campos
    if 'apellido' in body: persona.apellido = body['apellido']
    if 'usuario_suscripcion' in body: persona.usuario_suscripcion = body['usuario_suscripcion']
    if 'artista_nombre_artistico' in body: persona.artista_nombre_artistico = body['artista_nomrbre_artistico']
    if 'artista_verificado' in body: persona.artista_nombre_artistico = body['artista_verificado']

    persona = Personas.update(persona)   #Se modifica persona
    if not persona: return 'Persona no se pudo actualizar.', 400
    else: return jsonify(persona.json()), 200


#DELETE PERSONA
@app.route('/api/persona/<id>', methods=['DELETE'])
def delete_persona(id):
    persona = Personas.query.filter_by(id=id).first()
    if persona:
        persona.delete()
        return 'Persona eliminada.', 200
    else:
        return 'Persona no existe.', 404

#LISTA PERSONAS
@app.route("/api/persona/lista", methods=["GET"])
def get_personas():
    personas = Personas.query.order_by(Personas.id).all()
    return jsonify({"personas": [persona.json() for persona in personas]})

#===============================================================================#


#===============================================================================#
#CRUD CANCIONES
#===============================================================================#
#LISTA CANCIONEs
@app.route("/api/canciones/lista", methods=["GET"])
def get_canciones():
    canciones = Canciones.query.order_by(Canciones.id.asc()).all()
    return jsonify([cancion.json() for cancion in canciones])


#READ CANCION
@app.route('/api/canciones/<id>', methods=['GET'])
def get_cancion(id):
    cancion = Canciones.query.filter_by(id=id).first()

    if cancion:
        response = jsonify(cancion.json())
        return response
    else:
        return 'Canción no existe.', 404

#CREATE
@app.route('/api/canciones', methods=['POST'])
def put_cancion():
    body = request.get_json()
    cancion = Canciones()

    #Se asume que al crear se mandan todas las keys, por lo tanto no se revisa si existen
    if body.get('nombre') is not None and body.get('nombre').replace(" ", ""):
        cancion.nombre = body['nombre']
        cancion.letra = body['letra']
        cancion.fecha_composicion = body['fecha_composicion']
    else:
        return 'Canción DEBE tener nombre.', 400

    cancion = Canciones.create(cancion)   #se crea canción
    response = jsonify(cancion.json())
    return response, 201

#UPDATE CANCION
@app.route('/api/canciones/<id>', methods=['PUT'])
def edit_cancion(id):
    body = request.get_json()    #se obtienen datos actuales de persona
    cancion = Canciones.query.filter_by(id=id).first()
    if not cancion:
        return 'Canción no existe', 404

    if body.get('nombre') is None:
        if 'nombre' in body:
            return 'Canción DEBE tener nombre', 400
    else:
        if body.get('nombre').replace(" ", "") == '':
            return 'Canción DEBE tener nombre', 400
        else:
            cancion.nombre = body['nombre']

    #Se actualizan campos no obligatorios
    if 'letra' in body: cancion.letra = body['letra']
    if 'fecha_composicion' in body: cancion.fecha_composicion = body['fecha_composicion']

    cancion = Canciones.update(cancion)        #se modifica persona
    if not cancion: 
        return 'Canción no se pudo actualizar.', 400
    else: 
        return jsonify(cancion.json()), 200

#DELETE CANCION
@app.route('/api/canciones/<id>', methods=['DELETE'])
def delete_cancion(id):
    cancion = Canciones.query.filter_by(id=id).first()
    if not cancion:
        return 'Canción no existe.', 404
    else:
        nombre = cancion.nombre
        if cancion.delete():
            return 'Canción "'+ nombre + '" eliminada', 200
#===============================================================================#



#===============================================================================#
#CRUD FACTURAS
#===============================================================================#
#LISTA FACTURAS
@app.route("/api/facturas/lista", methods=["GET"])
def get_facturas():
    facturas = Facturas.query.order_by(Facturas.id.asc()).all()
    return jsonify({'facturas': [factura.json() for factura in facturas]})

#READ FACTURA
@app.route('/api/facturas/<id_factura>', methods=['GET'])
def get_factura(id_factura):
    factura = Facturas.query.filter_by(id=id_factura).first()

    if factura:
        return jsonify(factura.json())
    else:
        return 'Error. Factura no existe.', 404


#CREATE FACTURA
@app.route('/api/facturas', methods=['POST'])
def put_factura():
    body = request.get_json()
    factura = Facturas()

    #fecha de facturacion se saca del dia en que se ingresa si es que no se ingresa manualmente
    if body.get('fecha_facturacion') is not None:
        factura.fecha_facturacion = body['fecha_facturacion']
    else:
        factura.fecha_facturacion = datetime.today().strftime('%Y-%m-%d')
    if 'id_persona' in body:
        if not Personas.query.filter_by(id = body.get('id_persona')).first():
            return 'Error. el id_persona ingresado no existe.', 404
        else:
            factura.id_persona = body['id_persona']
    if 'fecha_vencimiento' in body:
        factura.fecha_vencimiento = body['fecha_vencimiento']
    if 'monto_facturado' in body:
        factura.monto_facturado = body['monto_facturado']
    if 'metodo_de_pago' in body:
        factura.metodo_de_pago = body['metodo_de_pago']

    #se asume que si se esta creando la factura, no esta pagada todavia
    factura.fecha_hora_pago = None
    factura.estado = False

    factura = Facturas.create(factura)
    if factura:
        return jsonify(factura.json())
    else:
        return 'Error. Factura no fue creada.', 400


#UPDATE FACTURA
@app.route('/api/facturas/<id_factura>', methods=['PUT'])
def edit_factura(id_factura):
    body = request.get_json()
    #se obtienen datos actuales de factura
    factura = Facturas.query.filter_by(id=id_factura).first()
    if not factura:
        return 'Factura que se busca no existe.', 404
    
    #puede ser que se cambien algunos atributos
    #asummiendo que se va a actualizar para una factura pagada, se cambia solo el estado y de ahi se saca la fecha
    if 'id_persona' in body:
        if not Personas.query.filter_by(id = body.get('id_persona')).first():
            return 'Error. el id_persona ingresado no existe.', 404
        else:
            factura.id_persona = body['id_persona']
    if 'fecha_facturacion' in body:
        factura.fecha_facturacion = body['fecha_facturacion']
    if 'fecha_vencimiento' in body:
        factura.fecha_vencimiento = body['fecha_vencimiento']
    if 'metodo_de_pago' in body:
        factura.metodo_de_pago = body['metodo_de_pago']
    if body.get('estado'):
        factura.estado = body['estado']
        factura.fecha_hora_pago = datetime.today()

    factura = Facturas.update(factura)    #se modifica factura
    if not factura:
        return 'Error. Factura no actualizada.', 400
    else:
        return jsonify(factura.json()), 200


#DELETE FACTURA
@app.route('/api/facturas/<id_factura>', methods=['DELETE'])
def delete_factura(id_factura):
    factura = Facturas.query.filter_by(id = id_factura).first()
    if not factura:
        return 'Error. Factura no existe.', 404
    else:
        factura.delete()
        return 'Factura eliminada.', 200
    
#===============================================================================#


#===============================================================================#
#CRUD REPRODUCCIONES
#===============================================================================#
#READ REPRODUCCION
@app.route('/api/reproducciones/<id_cancion>/<id_persona>', methods=['GET'])
def get_reproduccion(id_cancion, id_persona):
    reproduccion = Reproducciones.query.filter_by(id_persona=id_persona, id_cancion = id_cancion).first()

    if reproduccion:
        response = jsonify(reproduccion.json())
        return response
    else:
        return 'Reproducción no existe.', 404


#CREATE REPRODUCCION
@app.route('/api/reproducciones/<id_cancion>/<id_persona>', methods=['POST'])
def put_reproduccion(id_cancion, id_persona):

    if not Personas.query.filter_by(id = id_persona).first() or not Canciones.query.filter_by(id = id_cancion).first():
        return 'Error. Los IDs ingresados no existen.'
    elif Reproducciones.query.filter_by(id_persona=id_persona, id_cancion = id_cancion).first():
        return 'Error. Reproducción ya existe.'
    else:
        reproduccion = Reproducciones()
        reproduccion.id_persona = id_persona
        reproduccion.id_cancion = id_cancion
        reproduccion.cantidad_reproducciones = 1
        reproduccion.ultima_reproduccion = datetime.now(tz=None)

        reproduccion = Reproducciones.create(reproduccion)

    return jsonify(reproduccion.json())


#UPDATE REPRODUCCION 
@app.route('/api/reproducciones/<id_cancion>/<id_persona>', methods=['PUT'])
def edit_reproduccion(id_cancion, id_persona):
    reproduccion = Reproducciones.query.filter_by(id_cancion=id_cancion, id_persona = id_persona).first()

    #no se incluye editar ids, ya que solo se actualizan los datos de la relacion
    #se asume que si se quiere actualizar, es para aumentar 1 reproduccion
    if not reproduccion:
        return 'Reproducción no existe.', 404
    else:
        reproduccion.cantidad_reproducciones = reproduccion.cantidad_reproducciones + 1
        reproduccion.ultima_reproduccion = datetime.now(tz=None)

    reproduccion_update = Reproducciones.update(reproduccion)
    if not reproduccion_update:
        return 'Reproducción no actualizada.', 400
    else:
        response = jsonify(reproduccion_update.json())
    return response


#DELETE REPRODUCCION
@app.route('/api/reproducciones/<id_cancion>/<id_persona>', methods=['DELETE'])
def delete_reproduccion(id_cancion, id_persona):
    reproduccion = Reproducciones.query.filter_by(id_persona=id_persona, id_cancion = id_cancion).first()

    if reproduccion:
        reproduccion.delete()
        return 'Reproducción eliminada', 200
    else:
        return 'Reproducción no encontrada.', 400

#===============================================================================#

#USUARIO MOROSO
@app.route('/api/personas/moroso/<id_persona>', methods=['GET'])
def usuario_moroso(id_persona):
    if not Personas.query.filter_by(id=id_persona).first():
        return 'Persona no existe.', 404
    today = datetime.today().strftime('%Y-%m-%d')
    moroso = db.session.query(Facturas.id, 
                              Facturas.fecha_facturacion, 
                              Facturas.fecha_vencimiento, 
                              Facturas.monto_facturado).filter(
                                Facturas.id_persona == id_persona, 
                                Facturas.fecha_vencimiento < today, 
                                Facturas.estado == False).all()

    result = list()
    for factura in moroso:
        id, facturacion, vencimiento, monto = factura
        result.append({"id" : id, "monto_facturado" : monto, "fecha_facturacion" : facturacion.strftime('%d-%m-%Y'), "fecha_vencimiento" : vencimiento.strftime('%d-%m-%Y')})
    
    if result: 
        return jsonify({"mensaje": "El usuario tiene facturas vencidas", "facturas" : result})
    else:
        return jsonify({"mensaje": "El usuario no tiene facturas vencidas :)"})


#DEUDORES
@app.route('/api/facturas/deudores_cantidad', methods=['GET'])
def deudores():
    #dia actual
    today = datetime.today().strftime('%Y-%m-%d')

    #subtabla en la que están los deudores
    subquery = Facturas.query.filter(Facturas.fecha_vencimiento < today, 
                                     Facturas.estado == False).subquery()
    
    #suma obtiene la suma de todos los montos, distinct obtiene la cantidad de personas diferentes en la subtabla
    suma = db.session.query(db.func.sum(subquery.c.monto_facturado)).scalar()
    distinct = db.session.query(subquery).distinct(subquery.c.id_persona).count()

    #si es que suma es null, significa que se le debe 0 dinero a la empresa
    if not suma:
        suma = 0

    return jsonify({"qty_personas" : distinct, "qty_dinero" : suma})

#ULTIMO MES
@app.route('/api/facturas/ultimo-mes', methods=['GET'])
def ultimo_mes():
    mes = datetime.today() - timedelta(days=31)
    result = db.session.query(db.func.sum(Facturas.monto_facturado)).filter(Facturas.fecha_hora_pago > mes).scalar()
    
    if not result:
        result = 0

    return jsonify({"qty_dinero" : result})


#TOP 10
@app.route('/api/top10/<id_persona>', methods=['GET'])
def top10_usuario(id_persona):
    top_query = db.session.query(Reproducciones.id_cancion, 
                           Reproducciones.cantidad_reproducciones.label('reproducciones'), 
                           Canciones.nombre).filter_by(id_persona = id_persona).join(Canciones.reproducciones).order_by(Reproducciones.cantidad_reproducciones.desc()).limit(10)
    
    top = list()
    for cancion in top_query:
        top.append(dict(cancion))
    if top: 
        return jsonify({'top-ten':top})
    else:   
        return 'Usuario no ha escuchado canciones :('


#TOP 10 GLOBALES
@app.route('/api/top10/', methods=['GET'])
def top10_global():
    top_query = db.session.query(Reproducciones.id_cancion, 
                                Canciones.nombre, 
                                db.func.sum(Reproducciones.cantidad_reproducciones).label("reproducciones_totales")).join(
                                Canciones).group_by(
                                Reproducciones.id_cancion, Canciones.nombre).order_by(db.func.sum(Reproducciones.cantidad_reproducciones).desc()).limit(10).all()
    top = list()
    for cancion in top_query:
        top.append(dict(cancion))
    return jsonify({'top-ten-global':top})


if __name__ == '__main__':
	app.run(debug=True)
