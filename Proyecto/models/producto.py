from db import db
from models.producto_ingredientes import producto_ingredientes
from models.ingredientes import Ingredientes

class Producto(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    tipo_vaso = db.Column(db.String(50), nullable=True)
    volumen = db.Column(db.Float, nullable=True)
    heladeria_id = db.Column(db.Integer, db.ForeignKey('heladeria.id'), nullable=False)
    tipo_producto = db.Column(db.Enum('Copa', 'Malteada'), nullable=False)

    ingredientes = db.relationship('Ingredientes', secondary=producto_ingredientes, lazy='subquery',
                                   backref=db.backref('productos', lazy=True))

    def calcular_costo(self):
        return sum(ingrediente.precio for ingrediente in self.ingredientes)

    def calcular_calorias(self):
        total_calorias = sum(ingrediente.calorias for ingrediente in self.ingredientes) * 0.95
        return round(total_calorias, 2)

    def calcular_rentabilidad(self):
        return self.precio_publico - self.calcular_costo()

    def __repr__(self):
        return f'<Producto {self.nombre}>'