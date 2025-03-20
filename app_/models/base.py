from app_.config.db import db
from marshmallow import fields, Schema


class Base(db.Model):
    __tablename__ = "bases"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Integer, nullable=False)
    es_vegetariano = db.Column(db.Boolean, default=True)
    sabor = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Base {self.nombre}>"

    def abastecer(self):
        print(self.inventario)
        self.inventario += 5
        db.session.add(self)
        db.session.commit()
        print(self.inventario)

    def renovar_inventario(self):
        self.inventario = 0
        db.session.add(self)
        db.session.commit()


class BaseSchema(Schema):
    id = fields.Int()
    nombre = fields.Str()
    precio = fields.Float()
    calorias = fields.Int()
    inventario = fields.Int()