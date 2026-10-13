import math
import os

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect, CSRFError

from basededatos.conexion import obtener_opciones
from usuarios.usuario import Usuario
from usuarios.gestor_usuarios import GestorUsuarios
from videojuegos.Juegos.videojuego import Videojuego
from videojuegos.Juegos.tipos import TIPOS
from videojuegos.gestor_videojuegos import GestorVideojuegos
from solicitudes.solicitud import Solicitud
from solicitudes.gestor_solicitudes import GestorSolicitudes
from notificaciones.gestor_notificaciones import GestorNotificaciones

app = Flask(__name__)

# La clave secreta NO se escribe en el código: se lee de la variable de entorno GAMEHUB_SECRET_KEY.
# Si no existe (o es muy corta), la página no enciende, para no usar una clave insegura.
clave = os.environ.get("GAMEHUB_SECRET_KEY", "")
if len(clave) < 32:
    raise RuntimeError("Falta la variable de entorno GAMEHUB_SECRET_KEY (mínimo 32 caracteres). "
                       "Mira los pasos en LEEME.md.")
app.secret_key = clave
app.config["SESSION_COOKIE_HTTPONLY"] = True      # JavaScript no puede leer la cookie de sesión
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"     # otras páginas no pueden usar tu sesión

# Protección CSRF (Flask-WTF): cada formulario POST lleva un código secreto (csrf_token)
csrf = CSRFProtect(app)

gestor_usuarios = GestorUsuarios()
gestor_juegos = GestorVideojuegos()
gestor_solicitudes = GestorSolicitudes()
gestor_notificaciones = GestorNotificaciones()


# Cuenta los avisos sin leer para mostrar el número en el menú de todas las páginas
@app.context_processor
def contar_avisos():
    if "id_usuario" in session:
        try:
            return {"sin_leer": gestor_notificaciones.contar_sin_leer(session["id_usuario"])}
        except Exception:
            return {"sin_leer": 0}
    return {"sin_leer": 0}


# Muestra el precio con puntos de miles: 200000 -> 200.000
@app.template_filter("pesos")
def formato_pesos(valor):
    texto = "{:,}".format(int(valor))      # 200000 -> "200,000"
    return texto.replace(",", ".")          # "200,000" -> "200.000"


# Si alguien entra sin iniciar sesión, lo manda a la página de login
def ir_a_login():
    flash("Primero inicia sesión.", "error")
    return redirect(url_for("iniciar_sesion"))


# El rol de administrador se revisa en la BASE DE DATOS (en el servidor),
# no solo en la sesión ni ocultando botones.
def es_admin_actual():
    if "id_usuario" not in session:
        return False
    usuario = gestor_usuarios.buscar(session["id_usuario"])
    return usuario is not None and usuario.es_admin()


# Lee un número del formulario sin que la página se caiga si escriben letras
def leer_numero(texto, mensaje_error):
    try:
        numero = float(texto or 0)
    except ValueError:
        raise ValueError(mensaje_error)
    if not math.isfinite(numero):
        raise ValueError(mensaje_error)
    return numero


def validar_precio(precio):
    if precio < 0 or precio > 99999999:
        raise ValueError("El precio debe estar entre 0 y 99.999.999")


def validar_imagen(imagen):
    # La portada es opcional; si la ponen, debe ser un link web
    if imagen != "" and not imagen.startswith(("http://", "https://")):
        raise ValueError("La portada debe ser un link que empiece por http:// o https://")
    if len(imagen) > 500:
        raise ValueError("El link de la portada es muy largo")


# =====================================================
# ERRORES: mensajes amables, sin mostrar detalles de SQL Server
# =====================================================

@app.errorhandler(CSRFError)
def error_csrf(error):
    flash("El formulario venció o no es válido. Recarga la página e inténtalo otra vez.", "error")
    return redirect(request.referrer or url_for("inicio"))


@app.errorhandler(400)
def error_400(error):
    return render_template("error.html", titulo="Solicitud no válida",
                           texto="Faltan datos en el formulario. Vuelve e inténtalo de nuevo."), 400


@app.errorhandler(404)
def error_404(error):
    return render_template("error.html", titulo="Página no encontrada",
                           texto="Esa página no existe en GameHub."), 404


@app.errorhandler(500)
def error_500(error):
    return render_template("error.html", titulo="Algo salió mal",
                           texto="Tuvimos un problema con el servidor. Inténtalo en un momento."), 500


# =====================================================
# 1. PÁGINAS PARA TODOS (visitantes)
# =====================================================

# Página de inicio: muestra los últimos juegos
@app.route("/")
def inicio():
    juegos = gestor_juegos.listar_disponibles()
    return render_template("inicio.html", total=len(juegos), recientes=juegos[:4])


# Catálogo: todos los juegos disponibles (y el buscador)
@app.route("/catalogo")
def catalogo():
    buscar = request.args.get("buscar", "")
    plataforma = request.args.get("plataforma", "")
    todos = gestor_juegos.listar_disponibles()

    # El juego destacado es el más reciente
    destacado = None
    if len(todos) > 0:
        destacado = todos[0]

    # Filtra por nombre y por plataforma
    juegos = []
    for juego in todos:
        if buscar.lower() in juego.nombre.lower():
            if plataforma == "" or juego.plataforma == plataforma:
                juegos.append(juego)

    return render_template("catalogo.html", juegos=juegos, buscar=buscar, plataforma=plataforma,
                           destacado=destacado, plataformas=obtener_opciones("plataformas"))


# Crear cuenta: guarda un usuario nuevo y avisa al administrador
@app.route("/crear-cuenta", methods=["GET", "POST"])
def crear_cuenta():
    if request.method == "POST":
        usuario = Usuario(request.form["nombre"].strip(), request.form["correo"].strip().lower(),
                          request.form["telefono"].strip(), request.form["contrasena"])
        try:
            gestor_usuarios.agregar(usuario)
            gestor_notificaciones.enviar_a_administradores("Nuevo usuario registrado: " + usuario.nombre + ".")
            flash("Tu cuenta se creó. Ahora inicia sesión.", "ok")
            return redirect(url_for("iniciar_sesion"))
        except ValueError as error:
            flash(str(error), "error")
    return render_template("crear_cuenta.html")


# Iniciar sesión: revisa correo y contraseña y guarda el rol en la sesión
@app.route("/iniciar-sesion", methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == "POST":
        usuario = gestor_usuarios.iniciar_sesion(request.form["correo"].strip().lower(), request.form["contrasena"])
        if usuario is None:
            flash("Correo o contraseña incorrectos.", "error")
        else:
            # Se borra la sesión anterior y se guarda quién entró y qué rol tiene
            session.clear()
            session["id_usuario"] = usuario.id_usuario
            session["nombre"] = usuario.nombre
            session["rol"] = usuario.rol
            flash("Hola, " + usuario.nombre + ". " + usuario.descripcion(), "ok")
            if usuario.es_admin():
                return redirect(url_for("admin"))
            return redirect(url_for("catalogo"))
    return render_template("iniciar_sesion.html")


# Cerrar sesión: borra los datos de la sesión.
# Es POST (con csrf_token) para que otra página no pueda cerrarte la sesión con un simple link.
@app.route("/cerrar-sesion", methods=["POST"])
def cerrar_sesion():
    session.clear()
    flash("Cerraste sesión.", "ok")
    return redirect(url_for("inicio"))


# =====================================================
# 2. PÁGINAS DEL USUARIO (publicar y pedir juegos)
# =====================================================

# Publicar: crea un objeto de la clase hija elegida y lo guarda (CREATE)
@app.route("/publicar", methods=["GET", "POST"])
def publicar():
    if "id_usuario" not in session:
        return ir_a_login()

    if request.method == "POST":
        try:
            # Validaciones en el servidor (no basta con el HTML)
            nombre = request.form["nombre"].strip()
            if nombre == "" or len(nombre) > 100:
                raise ValueError("Escribe el nombre del juego (máximo 100 caracteres)")
            if request.form["tipo"] not in TIPOS:
                raise ValueError("Elige un tipo de juego de la lista")
            if request.form["genero"] not in obtener_opciones("generos") \
                    or request.form["plataforma"] not in obtener_opciones("plataformas") \
                    or request.form["desarrollador"] not in obtener_opciones("desarrolladores"):
                raise ValueError("Elige género, plataforma y desarrollador de las listas")
            if request.form["estado"] not in Videojuego.Estados or request.form["oferta"] not in Videojuego.Ofertas:
                raise ValueError("Elige el estado y el tipo de oferta de las listas")
            try:
                anio = int(request.form["anio"])
            except ValueError:
                raise ValueError("El año de lanzamiento no es válido")
            precio = leer_numero(request.form["precio"], "El precio no es válido")
            validar_precio(precio)
            imagen = request.form.get("imagen", "").strip()     # la portada es opcional
            validar_imagen(imagen)

            clase = TIPOS[request.form["tipo"]]
            juego = clase(nombre, request.form["genero"], request.form["plataforma"],
                          anio, precio, request.form["desarrollador"], request.form["estado"],
                          request.form["oferta"], session["id_usuario"])
            juego.imagen = imagen
            gestor_juegos.agregar(juego)
            gestor_notificaciones.enviar_a_administradores(session["nombre"] + " publicó el juego " + juego.nombre + ".")
            flash("Publicaste " + juego.nombre + ". " + juego.jugar(), "ok")
            return redirect(url_for("mis_juegos"))
        except ValueError as error:
            flash(str(error), "error")

    return render_template("publicar.html",
                           tipos=TIPOS.keys(),
                           generos=obtener_opciones("generos"),
                           plataformas=obtener_opciones("plataformas"),
                           desarrolladores=obtener_opciones("desarrolladores"),
                           estados=Videojuego.Estados,
                           ofertas=Videojuego.Ofertas)


# Mis juegos: solo los juegos del usuario que inició sesión (READ)
@app.route("/mis-juegos")
def mis_juegos():
    if "id_usuario" not in session:
        return ir_a_login()
    juegos = gestor_juegos.listar_de_usuario(session["id_usuario"])
    return render_template("mis_juegos.html", juegos=juegos)


# Cambiar precio de un juego propio (UPDATE)
@app.route("/juego/<int:id_videojuego>/precio", methods=["POST"])
def cambiar_precio(id_videojuego):
    if "id_usuario" not in session:
        return ir_a_login()
    juego = gestor_juegos.buscar(id_videojuego)
    if juego is None or juego.id_usuario != session["id_usuario"]:
        flash("Solo puedes cambiar el precio de tus juegos.", "error")
    elif not juego.disponible:
        flash("No puedes cambiar el precio: el juego está reservado para un comprador.", "error")
    else:
        try:
            precio = leer_numero(request.form["precio"], "El precio no es válido")
            validar_precio(precio)
            juego.cambiar_precio(precio)
            gestor_juegos.actualizar_precio(juego)
            flash("Precio actualizado.", "ok")
        except ValueError as error:
            flash(str(error), "error")
    return redirect(url_for("mis_juegos"))


# Cambiar la portada (link de imagen) de un juego propio (UPDATE)
@app.route("/juego/<int:id_videojuego>/imagen", methods=["POST"])
def cambiar_imagen(id_videojuego):
    if "id_usuario" not in session:
        return ir_a_login()
    juego = gestor_juegos.buscar(id_videojuego)
    if juego is None or juego.id_usuario != session["id_usuario"]:
        flash("Solo puedes cambiar la portada de tus juegos.", "error")
    else:
        try:
            imagen = request.form["imagen"].strip()
            validar_imagen(imagen)
            juego.imagen = imagen
            gestor_juegos.actualizar_imagen(juego)
            flash("Portada actualizada.", "ok")
        except ValueError as error:
            flash(str(error), "error")
    return redirect(url_for("mis_juegos"))


# Eliminar un juego: el dueño o el administrador (DELETE)
@app.route("/juego/<int:id_videojuego>/eliminar", methods=["POST"])
def eliminar_juego(id_videojuego):
    if "id_usuario" not in session:
        return ir_a_login()
    juego = gestor_juegos.buscar(id_videojuego)
    es_admin = es_admin_actual()

    try:
        if juego is None:
            flash("Ese juego no existe.", "error")
        elif juego.id_usuario == session["id_usuario"]:
            gestor_juegos.eliminar(id_videojuego)
            flash("Eliminaste " + juego.nombre + ".", "ok")
        elif es_admin:
            gestor_juegos.eliminar(id_videojuego)
            gestor_notificaciones.enviar(juego.id_usuario, "El administrador eliminó tu juego " + juego.nombre + ".")
            flash("Eliminaste " + juego.nombre + ". Se le avisó al dueño.", "ok")
        else:
            flash("Solo puedes eliminar tus juegos.", "error")
    except ValueError as error:
        # Juego con pedido aceptado: se conserva para el historial
        flash(str(error), "error")

    if es_admin:
        return redirect(url_for("admin"))
    return redirect(url_for("mis_juegos"))


# Pedir un juego: guarda la solicitud y le avisa al dueño
@app.route("/juego/<int:id_videojuego>/pedir", methods=["POST"])
def pedir_juego(id_videojuego):
    if "id_usuario" not in session:
        return ir_a_login()
    juego = gestor_juegos.buscar(id_videojuego)

    if juego is None or not juego.disponible:
        flash("Ese juego ya no está disponible.", "error")
    elif juego.id_usuario == session["id_usuario"]:
        flash("No puedes pedir tu propio juego.", "error")
    elif gestor_solicitudes.tiene_pendiente(id_videojuego, session["id_usuario"]):
        flash("Ya pediste este juego. Espera la respuesta del dueño.", "error")
    else:
        try:
            # 1. Se guarda la solicitud
            solicitud = Solicitud(id_videojuego, session["id_usuario"], request.form.get("mensaje", ""))
            gestor_solicitudes.agregar(solicitud)
            # 2. Se le avisa al dueño del juego
            gestor_notificaciones.enviar(juego.id_usuario,
                                         session["nombre"] + " quiere tu juego " + juego.nombre + ". Revisa tus solicitudes.")
            flash("Listo, le avisamos a " + juego.dueno + ". Te llegará una notificación con su respuesta.", "ok")
        except ValueError as error:
            flash(str(error), "error")
    return redirect(url_for("catalogo"))


# Solicitudes: las que me hicieron y las que yo hice
@app.route("/solicitudes")
def solicitudes():
    if "id_usuario" not in session:
        return ir_a_login()
    recibidas = gestor_solicitudes.listar_recibidas(session["id_usuario"])
    enviadas = gestor_solicitudes.listar_enviadas(session["id_usuario"])
    return render_template("solicitudes.html", recibidas=recibidas, enviadas=enviadas)


# Aceptar: el juego queda RESERVADO (sale del catálogo) y se le avisa al que lo pidió.
# Todo pasa en una transacción (GestorSolicitudes.aceptar), así no se aceptan dos pedidos del mismo juego.
@app.route("/solicitud/<int:id_solicitud>/aceptar", methods=["POST"])
def aceptar_solicitud(id_solicitud):
    if "id_usuario" not in session:
        return ir_a_login()
    solicitud = gestor_solicitudes.buscar(id_solicitud)
    if solicitud is None or solicitud.id_dueno != session["id_usuario"]:
        flash("Esa solicitud no es tuya.", "error")
    else:
        try:
            rechazados = gestor_solicitudes.aceptar(id_solicitud, solicitud.id_videojuego)
            dueno = gestor_usuarios.buscar(session["id_usuario"])
            gestor_notificaciones.enviar(solicitud.id_solicitante,
                                         dueno.nombre + " aceptó tu pedido de " + solicitud.nombre_juego +
                                         ". Escríbele al " + str(dueno.telefono) + " para ponerse de acuerdo.")
            # A los demás que pidieron el mismo juego se les avisa que ya no está disponible
            for id_persona in rechazados:
                gestor_notificaciones.enviar(id_persona, "El juego " + solicitud.nombre_juego +
                                             " ya fue reservado para otra persona. Tu pedido se cerró.")
            flash("Aceptaste. Le avisamos a " + solicitud.nombre_solicitante + ".", "ok")
        except ValueError as error:
            flash(str(error), "error")
    return redirect(url_for("solicitudes"))


# Rechazar: se le avisa al que lo pidió
@app.route("/solicitud/<int:id_solicitud>/rechazar", methods=["POST"])
def rechazar_solicitud(id_solicitud):
    if "id_usuario" not in session:
        return ir_a_login()
    solicitud = gestor_solicitudes.buscar(id_solicitud)
    if solicitud is None or solicitud.id_dueno != session["id_usuario"]:
        flash("Esa solicitud no es tuya.", "error")
    else:
        try:
            gestor_solicitudes.rechazar(id_solicitud)
            gestor_notificaciones.enviar(solicitud.id_solicitante,
                                         session["nombre"] + " rechazó tu pedido de " + solicitud.nombre_juego + ".")
            flash("Rechazaste. Le avisamos a " + solicitud.nombre_solicitante + ".", "ok")
        except ValueError as error:
            flash(str(error), "error")
    return redirect(url_for("solicitudes"))


# Notificaciones: los avisos de la persona que inició sesión
@app.route("/notificaciones")
def notificaciones():
    if "id_usuario" not in session:
        return ir_a_login()
    avisos = gestor_notificaciones.listar(session["id_usuario"])
    return render_template("notificaciones.html", avisos=avisos)


# Marcar UNA notificación como leída
@app.route("/notificacion/<int:id_notificacion>/leida", methods=["POST"])
def marcar_leida(id_notificacion):
    if "id_usuario" not in session:
        return ir_a_login()
    gestor_notificaciones.marcar_leida(id_notificacion, session["id_usuario"])
    return redirect(url_for("notificaciones"))


# =====================================================
# 3. PÁGINA DEL ADMINISTRADOR (ve todo)
# =====================================================

# Panel del administrador: ve todos los usuarios, juegos y solicitudes
@app.route("/admin")
def admin():
    if not es_admin_actual():
        flash("Esta página es solo para el administrador.", "error")
        return redirect(url_for("inicio"))
    return render_template("admin.html",
                           usuarios=gestor_usuarios.listar(),
                           juegos=gestor_juegos.listar_todos(),
                           solicitudes=gestor_solicitudes.listar_todas())


# Restablecer contraseña: el administrador le pone una contraseña nueva a un usuario
@app.route("/admin/usuario/<int:id_usuario>/contrasena", methods=["POST"])
def restablecer_contrasena(id_usuario):
    if not es_admin_actual():
        flash("Esta acción es solo para el administrador.", "error")
        return redirect(url_for("inicio"))
    usuario = gestor_usuarios.buscar(id_usuario)
    if usuario is None:
        flash("Ese usuario no existe.", "error")
    else:
        try:
            gestor_usuarios.cambiar_contrasena(id_usuario, request.form["nueva"])
            gestor_notificaciones.enviar(id_usuario,
                                         "El administrador restableció tu contraseña. Pídesela y cámbiala cuando entres.")
            flash("Se restableció la contraseña de " + usuario.nombre + ". Ya le avisamos.", "ok")
        except ValueError as error:
            flash(str(error), "error")
    return redirect(url_for("admin"))
