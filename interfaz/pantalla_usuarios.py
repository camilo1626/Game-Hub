import tkinter as tk
from tkinter import messagebox

from interfaz.estilos import titulo, tarjeta, campo, boton, tabla, TARJETA, VERDE, ROJO
from usuarios.usuario import Usuario


def crear(padre, app):
    titulo(padre, "Usuarios")
    formulario = tarjeta(padre)
    nombre = campo(formulario, "Nombre", 0)
    telefono = campo(formulario, "Teléfono", 1)
    correo = campo(formulario, "Correo", 2)

    lista = tabla(padre, ("ID", "Nombre", "Teléfono", "Correo"))
    usuarios = app.gestor_usuarios.listar()
    for u in usuarios:
        lista.insert("", "end", values=(u[0], u[1], u[2], u[3]))

    def registrar():
        if nombre.get() == "" or telefono.get() == "" or correo.get() == "":
            messagebox.showwarning("GameHub", "Llene todos los campos")
            return
        usuario = Usuario(nombre.get(), telefono.get(), correo.get())
        app.gestor_usuarios.agregar(usuario)
        messagebox.showinfo("GameHub", "Usuario registrado")
        app.cargar_usuarios()
        app.recargar()

    def eliminar():
        seleccion = lista.selection()
        if not seleccion:
            messagebox.showwarning("GameHub", "Seleccione un usuario")
            return
        u = usuarios[lista.index(seleccion[0])]
        if messagebox.askyesno("GameHub", "¿Eliminar a " + u[1] + "?"):
            app.gestor_usuarios.eliminar(u[0])
            app.cargar_usuarios()
            app.recargar()

    botones = tk.Frame(formulario, bg=TARJETA)
    botones.grid(row=0, column=2, rowspan=3, padx=20)
    boton(botones, "Registrar", VERDE, registrar).pack(fill="x", pady=3)
    boton(botones, "Eliminar", ROJO, eliminar).pack(fill="x", pady=3)
