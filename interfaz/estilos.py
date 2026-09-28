import tkinter as tk
from tkinter import ttk

FONDO = "#15131f"
PANEL = "#221f33"
TARJETA = "#2d2945"
TEXTO = "#ffffff"
SUAVE = "#b9b3e0"
MORADO = "#7c5cff"
VERDE = "#2e9e6b"
ROJO = "#c0392b"


def aplicar_estilos(ventana):
    ventana.configure(bg=FONDO)
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure("Treeview", background=TARJETA, fieldbackground=TARJETA, foreground=TEXTO, rowheight=26)
    estilo.configure("Treeview.Heading", background=PANEL, foreground=SUAVE, font=("Arial", 10, "bold"))
    estilo.map("Treeview", background=[("selected", MORADO)])


def titulo(padre, texto):
    tk.Label(padre, text=texto, bg=FONDO, fg=TEXTO, font=("Arial", 18, "bold")).pack(anchor="w", pady=(10, 5))


def tarjeta(padre):
    marco = tk.Frame(padre, bg=TARJETA, padx=15, pady=15)
    marco.pack(fill="x", pady=5)
    return marco


def campo(padre, texto, fila, opciones=None):
    tk.Label(padre, text=texto, bg=TARJETA, fg=SUAVE).grid(row=fila, column=0, sticky="w", pady=4, padx=(0, 10))
    if opciones is None:
        entrada = tk.Entry(padre, width=30)
    else:
        entrada = ttk.Combobox(padre, values=opciones, state="readonly", width=28)
    entrada.grid(row=fila, column=1, pady=4)
    return entrada


def boton(padre, texto, color, accion):
    return tk.Button(padre, text=texto, bg=color, fg=TEXTO, font=("Arial", 10, "bold"),
                     relief="flat", padx=12, pady=6, cursor="hand2", command=accion)


def tabla(padre, columnas):
    t = ttk.Treeview(padre, columns=columnas, show="headings", height=8)
    for columna in columnas:
        t.heading(columna, text=columna)
        t.column(columna, width=110)
    t.pack(fill="both", expand=True, pady=5)
    return t
