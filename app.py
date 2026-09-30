from flask import Flask, render_template, request, redirect, url_for, flash, session

from basededatos.conexion import obtener_opciones
from videojuegos.gestor_videojuegos import GestorVideojuegos
from videojuegos.Juegos.videojuego import Videojuego
from videojuegos.Juegos.tipos import TIPOS
from usuarios.usuario import Usuario
from usuarios.gestor_usuarios import GestorUsuarios

app = Flask(__name__)
app.secret_key = "gamehub-2026"

gestor = GestorVideojuegos()
gestor_usuarios = GestorUsuarios()


@app.route("/")
def inicio():
    juegos = gestor.listar_todos()
    return render_template("inicio.html", total=len(juegos), recientes=juegos[:4])


@app.route("/catalogo")
def catalogo():
    buscar = request.args.get("buscar", "")
    juegos = []
    for juego in gestor.listar_todos():
        if buscar.lower() in juego.nombre.lower():
            juegos.append(juego)
    return render_template("catalogo.html", juegos=juegos, buscar=buscar)


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    if "id_usuario" not in session:
        flash("Inicia sesión para registrar un videojuego.", "error")
        return redirect(url_for("iniciar_sesion"))

    if request.method == "POST":
        try:
            clase = TIPOS[request.form["tipo"]]
            juego = clase(
                request.form["nombre"],
                request.form["genero"],
                request.form["plataforma"],
                int(request.form["anio"]),
                0,
                request.form["desarrollador"],
                request.form["estado"],
                request.form["oferta"],
                session["id_usuario"],
            )
            juego.cambiar_precio(float(request.form["precio"] or 0))
            gestor.agregar(juego)
            juego.jugar()
            flash(juego.nombre + " se registró correctamente.", "ok")
            return redirect(url_for("videojuegos"))
        except ValueError as error:
            flash("No se pudo registrar: " + str(error), "error")

    return render_template(
        "registrar.html",
        tipos=list(TIPOS.keys()),
        generos=obtener_opciones("generos"),
        plataformas=obtener_opciones("plataformas"),
        desarrolladores=obtener_opciones("desarrolladores"),
        estados=Videojuego.Estados,
        ofertas=Videojuego.Ofertas,
    )


@app.route("/videojuegos")
def videojuegos():
    juegos = gestor.listar_todos()
    return render_template("videojuegos.html", juegos=juegos)


@app.route("/videojuegos/<int:id_videojuego>/precio", methods=["POST"])
def editar_precio(id_videojuego):
    juego = gestor.buscar(id_videojuego)
    try:
        juego.cambiar_precio(float(request.form["precio"] or 0))
        gestor.actualizar(juego)
        flash("Se actualizó el precio de " + juego.nombre + ".", "ok")
    except ValueError as error:
        flash("No se pudo actualizar: " + str(error), "error")
    return redirect(url_for("videojuegos"))


@app.route("/videojuegos/<int:id_videojuego>/eliminar", methods=["POST"])
def eliminar(id_videojuego):
    juego = gestor.buscar(id_videojuego)
    gestor.eliminar(id_videojuego)
    flash(juego.nombre + " se eliminó.", "ok")
    return redirect(url_for("videojuegos"))


@app.route("/crear-cuenta", methods=["GET", "POST"])
def crear_cuenta():
    if request.method == "POST":
        usuario = Usuario(request.form["nombre"], request.form["correo"], request.form["contrasena"])
        try:
            gestor_usuarios.agregar(usuario)
            flash("Tu cuenta se creó. Ahora inicia sesión.", "ok")
            return redirect(url_for("iniciar_sesion"))
        except ValueError as error:
            flash("No se pudo crear la cuenta: " + str(error), "error")
    return render_template("crear_cuenta.html")


@app.route("/iniciar-sesion", methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == "POST":
        usuario = gestor_usuarios.iniciar_sesion(request.form["correo"], request.form["contrasena"])
        if usuario is not None:
            session["id_usuario"] = usuario.id_usuario
            session["nombre"] = usuario.nombre
            flash("Bienvenido, " + usuario.nombre + ".", "ok")
            return redirect(url_for("inicio"))
        flash("Correo o contraseña incorrectos.", "error")
    return render_template("iniciar_sesion.html")


@app.route("/cerrar-sesion")
def cerrar_sesion():
    session.clear()
    flash("Cerraste sesión.", "ok")
    return redirect(url_for("inicio"))
