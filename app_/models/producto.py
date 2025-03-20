from app_.config.db import db, ma
from app_.models.base import Base
from app_.models.complemento import Complemento
from marshmallow import fields, Schema

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    tipo = db.Column(db.String(50))  # 'Copa' o 'Malteada'

class Ingrediente(db.Model):
    __tablename__ = "ingredientes"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50))  # 'base' o 'complemento'
    cantidad_necesaria = db.Column(db.Integer, nullable=False, default=1)

    producto = db.relationship("Producto", backref="ingredientes")

    def consumir(self, cantidad):
        if self.tipo == "base":
            ingrediente = Base.query.filter_by(nombre=self.nombre).first()
        elif self.tipo == "complemento":
            ingrediente = Complemento.query.filter_by(nombre=self.nombre).first()
        else:
            return False

        if ingrediente and ingrediente.inventario >= cantidad:
            ingrediente.inventario -= cantidad
            db.session.add(ingrediente)
            return True
        return False


class ProductoSchema(Schema):
    id = fields.Int()
    nombre = fields.Str()
    precio_publico = fields.Float()
    tipo = fields.Str()