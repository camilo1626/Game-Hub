import tkinter as tk
from tkinter import messagebox

from interfaz.estilos import titulo, tabla, boton, FONDO, VERDE, ROJO, MORADO


def crear(padre, app):
    id_usuario = app.usuario_actual.id_usuario

    titulo(padre, "Solicitudes recibidas")
    tabla_recibidas = tabla(padre, ("Mi juego", "Solicitante", "Teléfono", "Ofrece", "Estado"))
    recibidas = app.gestor_solicitudes.listar_recibidas(id_usuario)
    for s in recibidas:
        tabla_recibidas.insert("", "end", values=(s[1], s[2], s[3], s[4] or "-", s[5]))

    def elegida(tabla_actual, datos):
        seleccion = tabla_actual.selection()
        if not seleccion:
            messagebox.showwarning("GameHub", "Seleccione una solicitud")
            return None
        solicitud = datos[tabla_actual.index(seleccion[0])]
        if solicitud[5] != "Pendiente":
            messagebox.showinfo("GameHub", "Esta solicitud ya fue respondida")
            return None
        return solicitud

    def aceptar():
        s = elegida(tabla_recibidas, recibidas)
        if s:
            app.gestor_solicitudes.aceptar(s[0])
            messagebox.showinfo("GameHub", "Aceptada. Contacta a " + s[2] + " al " + s[3])
            app.recargar()

    def rechazar():
        s = elegida(tabla_recibidas, recibidas)
        if s:
            app.gestor_solicitudes.rechazar(s[0])
            app.recargar()

    botones = tk.Frame(padre, bg=FONDO)
    botones.pack(anchor="w")
    boton(botones, "Aceptar", VERDE, aceptar).pack(side="left", padx=(0, 5))
    boton(botones, "Rechazar", ROJO, rechazar).pack(side="left")

    titulo(padre, "Solicitudes enviadas")
    tabla_enviadas = tabla(padre, ("Juego", "Dueño", "Teléfono", "Ofrezco", "Estado"))
    enviadas = app.gestor_solicitudes.listar_enviadas(id_usuario)
    for s in enviadas:
        tabla_enviadas.insert("", "end", values=(s[1], s[2], s[3], s[4] or "-", s[5]))

    def cancelar():
        s = elegida(tabla_enviadas, enviadas)
        if s:
            app.gestor_solicitudes.eliminar(s[0])
            app.recargar()

    boton(padre, "Cancelar solicitud", MORADO, cancelar).pack(anchor="w")
