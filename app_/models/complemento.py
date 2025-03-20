from app_.config.db import db
from marshmallow import fields, Schema


class Complemento(db.Model):
    __tablename__ = "complementos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Integer, nullable=False)
    inventario = db.Column(db.Integer, nullable=False)
    es_vegetariano = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Complemento {self.nombre}>"

    def abastecer(self):
        self.inventario += 5
        db.session.add(self)
        db.session.commit()

    def renovar_inventario(self):
        self.inventario = 0
        db.session.add(self)
        db.session.commit()


class ComplementoSchema(Schema):
    id = fields.Int()
    nombre = fields.Str()
    precio = fields.Float()
    calorias = fields.Int()
    inventario = fields.Int()
