from app_.models.base import Base
from app_.models.complemento import Complemento
from app_.config.db import db


def contar_calorias(calorias_ingredientes):
    calorias_totales = sum(calorias_ingredientes) * 0.95
    return round(calorias_totales, 2)


def calcular_costo_ingredientes(ingredientes):
    costo_total = 0
    for ingrediente in ingredientes:
        if ingrediente.tipo == "base":
            base = Base.query.filter_by(nombre=ingrediente.nombre).first()
            if base:
                costo_total += base.precio
        elif ingrediente.tipo == "complemento":
            complemento = Complemento.query.filter_by(nombre=ingrediente.nombre).first()
            if complemento:
                costo_total += complemento.precio

    return round(costo_total, 2)


def calcular_rentabilidad(precio_publico, ingredientes):
    costo = calcular_costo_ingredientes(ingredientes)
    rentabilidad = precio_publico - costo
    return round(rentabilidad, 2)

def realizar_venta(producto, heladeria):
    for ingrediente in producto.ingredientes:
        if not ingrediente.consumir(ingrediente.cantidad_necesaria):
            raise ValueError(ingrediente.nombre)

    heladeria.ventas_diarias += producto.precio_publico
    db.session.commit()
    return "¡Vendido!"