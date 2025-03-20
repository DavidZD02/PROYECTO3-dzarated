from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app_.models.producto import Producto, ProductoSchema
from app_.models.base import Base
from app_.models.complemento import Complemento
from app_.models.heladeria import Heladeria
from app_.config.db import db
from app_.controllers.funciones import contar_calorias
from app_.controllers.funciones import calcular_costo_ingredientes
from app_.controllers.funciones import calcular_rentabilidad
from app_.controllers.funciones import realizar_venta
from app_.models.users import User
from app_.config.auth import login_manager


home_blueprint = Blueprint("home", __name__)

@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(str(user_id))


@home_blueprint.errorhandler(401)
def unauthorized(error):
    return render_template("error.html"), 401


@home_blueprint.route("/")
def home():
    return render_template("index.html")


@home_blueprint.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@home_blueprint.route("/dashboard")
@login_required
def dashboard():
    return render_template("index_admin.html")


@home_blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home.login"))


@home_blueprint.route("/login", methods=["GET", "POST"])
def auth():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username, password=password).first()

    if user:
        login_user(user)
        if user.is_admin:
            return redirect(url_for("home.dashboard"))
        return redirect(url_for("home.dashboard"))

    flash("Las credenciales no estan registradas en el sistema", "error")
    return redirect(url_for("home.login"))


@home_blueprint.route("/vender", methods=["GET", "POST"])
def vender_producto():
    if request.method == "POST":
        producto_id = request.form.get("producto_id")
        producto = Producto.query.get(producto_id)
        heladeria = Heladeria.query.get(1)

        if current_user.is_admin or current_user.is_employee:
            if producto:
                try:
                    mensaje = realizar_venta(producto, heladeria)
                    flash(mensaje, "success")
                except ValueError as e:
                    ingrediente_faltante = str(e)
                    flash(
                        f"¡Oh no! Nos hemos quedado sin {ingrediente_faltante}",
                        "danger",
                    )
            else:
                flash("Producto no encontrado.", "danger")

            return redirect(url_for("home.vender_producto"))
        else:
            flash("No tienes permisos para vender.", "danger")

    productos = Producto.query.all()
    heladeria = Heladeria.query.get(1)
    return render_template("vender.html", productos=productos, heladeria=heladeria)


@home_blueprint.route("/abastecer", methods=["GET", "POST"])
@login_required
def abastecer():
    if request.method == "POST":
        # Obtener datos del formulario
        base_id = request.form.get("base_id")
        complemento_id = request.form.get("complemento_id")
        complemento_reiniciar_id = request.form.get("complemento_reiniciar_id")
        base_reiniciar_id = request.form.get("base_reiniciar_id")

        # Abastecer base si existe
        if base_id:
            base = Base.query.get(base_id)
            if base:
                base.abastecer()
                flash(f"Base {base.nombre} abastecida correctamente.", "success")
            else:
                flash("La base seleccionada no existe.", "error")

        # Abastecer complemento si existe
        if complemento_id:
            complemento = Complemento.query.get(complemento_id)
            if complemento:
                complemento.abastecer()
                flash(
                    f"Complemento {complemento.nombre} abastecido correctamente.",
                    "success",
                )
            else:
                flash("El complemento seleccionado no existe.", "error")

        if complemento_reiniciar_id:
            complemento_reiniciar = Complemento.query.get(complemento_reiniciar_id)
            if complemento_reiniciar:
                complemento_reiniciar.renovar_inventario()
                flash(
                    "Inventario renovado.",
                    "success",
                )
            else:
                flash("El complemento seleccionado no existe.", "error")

        if base_reiniciar_id:
            base_reiniciar = Base.query.get(base_reiniciar_id)
            if base_reiniciar:
                base_reiniciar.renovar_inventario()
                flash(
                    "Inventario renovado.",
                    "success",
                )
            else:
                flash("El complemento seleccionado no existe.", "error")

        # Redirigir después de procesar ambos
        return redirect(url_for("home.abastecer"))

    # Obtener bases y complementos para mostrar en la página
    bases = Base.query.all()
    complementos = Complemento.query.all()
    return render_template("abastecer.html", bases=bases, complementos=complementos)


@home_blueprint.route("/info_productos", methods=["GET"])
@login_required
def info_productos():
    productos = Producto.query.all()
    productos_info = []

    for producto in productos:
        ingredientes = producto.ingredientes
        calorias_ingredientes = []
        for ing in ingredientes:
            if ing.tipo == "base":
                calorias = Base.query.filter_by(nombre=ing.nombre).first().calorias
            else:
                calorias = Complemento.query.filter_by(nombre=ing.nombre).first().calorias
            calorias_ingredientes.append(calorias)

        calorias = contar_calorias(calorias_ingredientes)

        # Calcular costo de producción
        costo = calcular_costo_ingredientes(ingredientes)

        # Calcular rentabilidad
        rentabilidad = calcular_rentabilidad(producto.precio_publico, ingredientes)

        # Agregar la información del producto
        productos_info.append(
            {
                "nombre": producto.nombre,
                "precio_publico": producto.precio_publico,
                "calorias_totales": calorias,
                "costo_produccion": costo,
                "rentabilidad": rentabilidad,
            }
        )

    return render_template("info_productos.html", productos_info=productos_info)
