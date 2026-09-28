from basededatos.conexion import probar_conexion
from interfaz.ventana import iniciar_interfaz

conectado, error = probar_conexion()

if conectado:
    iniciar_interfaz()
else:
    print("No se pudo conectar con SQL Server:")
    print(error)