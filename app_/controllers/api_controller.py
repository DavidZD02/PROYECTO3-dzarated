from flask import Blueprint, jsonify
from app_.models.producto import Producto, ProductoSchema
from app_.models.base import Base, BaseSchema
from app_.models.complemento import Complemento, ComplementoSchema
from app_.controllers.funciones import (
    contar_calorias,
    calcular_rentabilidad,
    calcular_costo_ingredientes,
)
from app_.config.db import db

api_blueprint = Blueprint("api", __name__)

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

base_schema = BaseSchema()
bases_schema = BaseSchema(many=True)

complemento_schema = ComplementoSchema()
complementos_schema = ComplementoSchema(many=True)


# Consultar todos los productos
@api_blueprint.route("/api/productos", methods=["GET"])
def get_productos():
    productos = Producto.query.all()  # Obtén todos los productos
    return jsonify(
        {
            "mensaje": "Productos", 
            "code": 200, 
            "data": productos_schema.dump(productos)}
        )


@api_blueprint.route("/api/productos/<int:id>", methods=["GET"])
def get_producto(id):
    producto = Producto.query.get_or_404(id)
    return jsonify(
        {
            "mensaje": "Producto Encontrado",
            "code": 200,
            "data": producto_schema.dump(producto),
        }
    )


# Consultar un producto por nombre
@api_blueprint.route("/api/productos/nombre/<string:nombre>", methods=["GET"])
def get_producto_by_nombre(nombre):
    producto = Producto.query.filter_by(nombre=nombre).first()
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(
        {
            "mensaje": "Producto encontrado",
            "code": 200,
            "data": producto_schema.dump(producto),
        }
    )


# Consultar las calorías de un producto por ID
@api_blueprint.route("/api/productos/<int:id>/calorias", methods=["GET"])
def get_calorias_producto(id):
    producto = Producto.query.get_or_404(id)
    ingredientes = producto.ingredientes
    calorias_ingredientes = []
    for ing in ingredientes:
        if ing.tipo == "base":
            calorias = Base.query.filter_by(nombre=ing.nombre).first().calorias
        else:
            calorias = Complemento.query.filter_by(nombre=ing.nombre).first().calorias
        calorias_ingredientes.append(calorias)

    calorias = contar_calorias(calorias_ingredientes)
    return jsonify(
        {
            "mensaje": "Producto encontrado",
            "code": 200,
            "data": {
                "id": producto.id,
                "nombre": producto.nombre,
                "calorias": calorias
            }
        }
    )


# Consultar la rentabilidad de un producto por ID
@api_blueprint.route("/api/productos/<int:id>/rentabilidad", methods=["GET"])
def get_rentabilidad_producto(id):
    producto = Producto.query.get_or_404(id)
    ingredientes = producto.ingredientes
    rentabilidad = calcular_rentabilidad(producto.precio_publico, ingredientes)
    return jsonify(
        {
            "mensaje": "Producto encontrado",
            "code": 200,
            "data": {
                "id": producto.id,
                "nombre": producto.nombre,
                "rentabilidad": rentabilidad
            }
        }
    )


# Consultar el costo de un producto por ID
@api_blueprint.route("/api/productos/<int:id>/costo", methods=["GET"])
def get_costo_producto(id):
    producto = Producto.query.get_or_404(id)
    ingredientes = producto.ingredientes
    costo = calcular_costo_ingredientes(ingredientes)
    return jsonify(
        {
            "mensaje": "Producto encontrado",
            "code": 200,
            "data": {
                "id": producto.id,
                "nombre": producto.nombre,
                "costo": costo
            }
        }
    )


# Vender un producto por ID
@api_blueprint.route("/api/productos/<int:id>/vender", methods=["POST"])
def vender_producto(id):
    producto = Producto.query.get_or_404(id)
    for ing in producto.ingredientes:
        if not ing.consumir(ing.cantidad_necesaria):
            return jsonify({"error": f"Falta inventario de {ing.nombre}"}), 400
    db.session.commit()
    return jsonify({"message": f"Producto {producto.nombre} vendido con éxito"}), 200


# Consultar todos los ingredientes
@api_blueprint.route("/api/ingredientes", methods=["GET"])
def get_ingredientes():
    bases = Base.query.all()
    complementos = Complemento.query.all()
    return jsonify(
        {
            "mensaje": "Ingredientes Encontrados",
            "code": 200,
            "data": {
                "bases": bases_schema.dump(bases),
                "complementos": complementos_schema.dump(complementos),
            },
        }
    )
