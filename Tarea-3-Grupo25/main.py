from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
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
CORS(app)


#CRUD PERSONAS
#===============================================================================#
#READ
@app.route('/api/persona/<id>', methods=['GET'])
def get_persona(id):
    persona = Personas.query.filter_by(id=id).first()
    if persona:
        response = jsonify(persona.json())
        return response
    else:
        return 'Persona no existe', 404


@app.route("/api/personas/lista", methods=["GET"])
def get_personas():
    personas = Personas.query.all()
    return jsonify([persona.json() for persona in personas])


#CREATE
@app.route('/api/persona', methods=['POST'])
def put_persona():
    body = request.get_json()
    persona = Personas()
    persona.nombre = body['nombre']
    persona.apellido = body['apellido']
    persona.email = body['email']
    persona.password = body['password']
    persona.tipo_de_persona = body['tipo_de_persona']

    persona = Personas.create(persona)
    response = jsonify(persona.json())

    return response


#UPDATE
@app.route('/api/persona/<id>', methods=['PUT'])
def editar_persona(id):
    body = request.get_json()
    #se obtienen datos actuales de persona
    persona = Personas.query.filter_by(id=id).first()

    #si alguna llave no viene, no se actualiza
    if 'nombre' in body:
        persona.nombre = body['nombre']
    if 'apellido' in body:
        persona.apellido = body['apellido']
    if 'email' in body:
        persona.email = body['email']
    if 'password' in body:
        persona.password = body['password']

    #se modifica persona
    persona = Personas.update(persona)
    if not persona:
        return 'Persona no se pudo actualizar', 400

    response = jsonify(persona.json())
    return response


#DELETE
@app.route('/api/persona/<id>', methods=['DELETE'])
def delete_persona(id):
    persona = Personas.query.filter_by(id=id).first()
    if persona:
        persona.delete()
        return 'Persona eliminada', 200
    else:
        return 'Persona no encontrada', 400

#===============================================================================#


#CRUD CANCIONES
#===============================================================================#
@app.route("/api/canciones/lista", methods=["GET"])
def get_canciones():
    canciones = Canciones.query.all()
    return jsonify([cancion.json() for cancion in canciones])



@app.route('/api/canciones/<id>', methods=['GET'])
def get_cancion(id):
    cancion = Canciones.query.filter_by(id=id).first()

    if cancion:
        response = jsonify(cancion.json())
        return response
    else:
        return 'Cancion no existe', 404

#CREATE
@app.route('/api/canciones', methods=['POST'])
def put_cancion():
    body = request.get_json()
    cancion = Canciones()
    cancion.nombre = body['nombre']
    cancion.letra = body['letra']
    cancion.fecha_composicion = body['fecha_composicion']

    cancion = Canciones.create(cancion)
    response = jsonify(cancion.json())

    return response


#UPDATE
@app.route('/api/canciones/<id>', methods=['PUT'])
def editar_cancion(id):
    body = request.get_json()
    #se obtienen datos actuales de persona
    cancion = Canciones.query.filter_by(id=id).first()

    #si alguna llave no viene, no se actualiza
    if 'nombre' in body:
        cancion.nombre = body['nombre']
    if 'letra' in body:
        cancion.letra = body['letra']
    if 'fecha_composicion' in body:
        cancion.fecha_composicion = body['fecha_composicion']

    #se modifica persona
    cancion = Canciones.update(cancion)
    if not cancion:
        return 'cancion no se pudo actualizar', 400

    response = jsonify(cancion.json())

    return response

#DELETE
@app.route('/api/canciones/<id>', methods=['DELETE'])
def delete_cancion(id):
    cancion = Canciones.query.filter_by(id=id).first()
    cancion.delete()
    return 'Canción eliminada', 200
#===============================================================================#



#CRUD REPRODUCCIONES

#===============================================================================#
#READ
@app.route('/api/reproducciones/<id_cancion>/<id_persona>', methods=['GET'])
def get_reproduccion(id_cancion, id_persona):
    reproduccion = Reproducciones.query.filter_by(id_persona=id_persona, id_cancion = id_cancion).first()

    if reproduccion:
        response = jsonify(reproduccion.json())
        return response
    else:
        return 'Reproduccion no existe', 404


#CREATE
@app.route('/api/reproducciones/<id_cancion>/<id_persona>', methods=['POST'])
def put_reproduccion(id_cancion, id_persona):
    dt = datetime.now(tz=None)
    reproduccion = Reproducciones()
    reproduccion.id_persona = id_persona
    reproduccion.id_cancion = id_cancion
    reproduccion.cantidad_reproducciones = 1
    reproduccion.ultima_reproduccion = dt

    reproduccion = Reproducciones.create(reproduccion)
    response = jsonify(reproduccion.json())

    return response


#UPDATE
@app.route('/api/reproducciones/<id_cancion>/<id_persona>', methods=['PUT'])
def editar_reproduccion(id_cancion, id_persona):
    body = request.get_json()
    #se obtienen datos actuales de reproduccion
    reproduccion = Reproducciones.query.filter_by(id_cancion=id_cancion, id_persona = id_persona).first()

    #si alguna llave no viene, no se actualiza
    #no se incluye editar ids, ya que solo se actualizan los datos de la relacion
    if not reproduccion:
        return 'Reproduccion no existe', 400

    if 'cantidad_reproducciones' in body:
        reproduccion.cantidad_reproducciones = body['cantidad_reproducciones']
    if 'ultima_reproduccion' in body:
        reproduccion.ultima_reproduccion = body['ultima_reproduccion']

    #se modifica persona
    reproduccion_update = Reproducciones.update(reproduccion)
    if not reproduccion_update:
        return 'Reproduccion no actualizada', 400
    else:
        response = jsonify(reproduccion_update.json())

    return response


#DELETE
@app.route('/api/reproducciones/<id_cancion>/<id_persona>', methods=['DELETE'])
def delete_reproduccion(id_cancion, id_persona):
    reproduccion = Reproducciones.query.filter_by(id_persona=id_persona, id_cancion = id_cancion).first()

    if reproduccion:
        reproduccion.delete()
        return jsonify({'mensaje':'reproduccion eliminada'})
    else:
        return 'Reproduccion no encontrada', 400
#===============================================================================#

#CRUD FACTURAS

#===============================================================================#
#READ
@app.route('/api/reproducciones/facturas/id', methods=['GET'])
def get_facturas(id):
    factura = Facturas.query.filter_by(id=id).first()

    if factura:
        response = jsonify(factura.json())
        return response
    else:
        return 'Factura no existe', 404


#CREATE
@app.route('/api/facturas', methods=['POST'])
def put_facturas():
    body = request.get_json()
    factura = Facturas()
    factura.id_persona = body['id_persona']
    factura.monto_facturado = body['monto_facturado']
    factura.fecha_facturacion = body['fecha_facturacion']
    factura.fecha_vencimiento = body['fecha_vencimiento']
    factura.fecha_hora_pago = body['fecha_hora_pago']
    factura.estado = body['estado']
    factura.metodo_de_pago = body['metodo_de_pago']

    factura = Reproducciones.create(factura)
    print(factura)
    response = jsonify(factura.json())
    print(response)

    return response


#UPDATE
@app.route('/api/reproducciones/<id_cancion>/<id_persona>', methods=['PUT'])
def editar_factura(id_cancion, id_persona):
    body = request.get_json()
    #se obtienen datos actuales de reproduccion
    reproduccion = Reproducciones.query.filter_by(id_cancion=id_cancion, id_persona = id_persona).first()

    #si alguna llave no viene, no se actualiza
    #no se incluye editar ids, ya que solo se actualizan los datos de la relacion
    if 'cantidad_reproducciones' in body:
        reproduccion.cantidad_reproducciones = body['cantidad_reproducciones']
    if 'ultima_reproduccion' in body:
        reproduccion.ultima_reproduccion = body['ultima_reproduccion']

    #se modifica persona
    reproduccion = Reproducciones.update(reproduccion)
    if not reproduccion:
        return 'Reproduccion no actualizada', 400

    response = jsonify(reproduccion.json())

    return response


#DELETE
@app.route('/api/reproducciones/<id_cancion>/<id_persona>', methods=['DELETE'])
def delete_factura(id_cancion, id_persona):
    reproduccion = Reproducciones.query.filter_by(id_persona=id_persona, id_cancion = id_cancion).first()

    reproduccion.delete()

    return jsonify({'mensaje':'reproduccion eliminada'})
#===============================================================================#

#TOP 10
@app.route('/api/top10/<id_persona>', methods=['GET'])
def top10_usuario(id_persona):
    top_query = db.session.query(Reproducciones.id_cancion, 
                           Reproducciones.cantidad_reproducciones.label('reproducciones'), 
                           Canciones.nombre).filter_by(id_persona = id_persona).join(Canciones).order_by(Reproducciones.cantidad_reproducciones.desc()).limit(10)
    
    if top_query:
        top = list()
        for cancion in top_query:
            top.append(dict(cancion))
        return jsonify({'top-ten':top})
    else:
        return 'Usuario no ha escuchado canciones'


if __name__ == '__main__':
	app.run(debug=True)



