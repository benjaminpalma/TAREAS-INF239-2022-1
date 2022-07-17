from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

db = SQLAlchemy()

#Creamos tablas
class Personas(db.Model):
    __tablename__='personas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100))
    email = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    usuario_suscripcion = db.Column(db.Boolean)
    artista_nombre_artistico = db.Column(db.String(100))
    artista_verificado = db.Column(db.Boolean)
    tipo_de_persona = db.Column(db.Boolean, nullable=False)
    
    facturas = db.relationship('Facturas', cascade='all, delete-orphan')
    reproducciones = db.relationship('Reproducciones', cascade='all, delete-orphan')

    @classmethod
    def create(cls, persona): 
        return persona.save()
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            #se devuelve a si mismo si es que se crea
            return self
        except:
            return False
    
    def update(self):
        return self.save()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return self
        except:
            return False

    
    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'password': self.password,
            'tipo_de_persona': self.tipo_de_persona,
            'usuario_suscripcion_activa' : self.usuario_suscripcion,
            'artista_nombre_artistico': self.artista_nombre_artistico, 
            'artista_verificado': self.artista_verificado
        }


class Canciones(db.Model):
    __tablename__ = 'canciones'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100), nullable = False)
    letra  = db.Column(db.String)
    fecha_composicion = db.Column(db.Date)
    
    reproducciones = db.relationship('Reproducciones', cascade='all, delete-orphan')
    

    @classmethod
    def create(cls, cancion):
        return cancion.save()

    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False
    
    def update(self):
        self.save()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return self
        except:
            return False
    
    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'letra': self.letra,
            'fecha_composicion': self.fecha_composicion
        }
    
class Facturas(db.Model):
    __tablename__ = 'facturas'
    id = db.Column(db.Integer, primary_key = True)
    monto_facturado = db.Column(db.Integer)
    metodo_de_pago = db.Column(db.String(100))
    estado = db.Column(db.Boolean)
    fecha_facturacion = db.Column(db.Date)
    fecha_vencimiento = db.Column(db.Date)
    fecha_hora_pago = db.Column(db.DateTime())
    id_persona = db.Column(db.Integer, db.ForeignKey('personas.id'))


    @classmethod
    def create(cls, factura):
        return factura.save()

        
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False
        
    def update(self):
        self.save()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return self
        except:
            return False
        
    def json(self):
        return {
            'id'                : self.id,
            'id_persona'        : self.id_persona,
            'monto_facturado'   : self.monto_facturado,
            'metodo_de_pago'    : self.metodo_de_pago,
            'estado'            : self.estado,
            'fecha_facturacion'  : self.fecha_facturacion,
            'fecha_vencimiento' : self.fecha_vencimiento,
            'fecha_hora_pago'   : self.fecha_hora_pago
        }

class Reproducciones(db.Model):
    __tablename__ = 'reproducciones'
    id_persona = db.Column(db.Integer, db.ForeignKey('personas.id'), primary_key = True)
    id_cancion = db.Column(db.Integer, db.ForeignKey('canciones.id'), primary_key = True)
    cantidad_reproducciones = db.Column(db.Integer)
    ultima_reproduccion = db.Column(db.DateTime())

    @classmethod
    def create(cls, reproduccion):
        return reproduccion.save()
        
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False
        
    def update(self):
        self.save()
        return self

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()

            return self
        except:
            return False
        
    def json(self):
        return {
            'id_persona': self.id_persona,
            'id_cancion': self.id_cancion,
            'cantidad_reproducciones': self.cantidad_reproducciones,
            'ultima_reproduccion': self.ultima_reproduccion
        }

def top10(id_persona):
    top = db.Query(Reproducciones).filter(Reproducciones.cantidad_reproducciones > 0)
    return top;