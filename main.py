from basededatos.conexion import probar_conexion
from app import app

conectado, error = probar_conexion()

if conectado:
    app.run(debug=True)
else:
    print("No se pudo conectar con SQL Server:")
    print(error)
