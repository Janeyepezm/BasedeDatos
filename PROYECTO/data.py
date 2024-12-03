import json

# Usuarios y contraseñas
USUARIOS = {
    "admin": "12345",
    "usuario1": "abcd1234",
    "empleado1": "pass123",
}

# Ruta del archivo JSON para guardar datos
RUTA_DATOS = "datos.json"

import json

import json

# Función para cargar los datos desde el archivo JSON
def cargar_datos():
    try:
        with open("datos.json", "r") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        # Si el archivo no existe, retornar la estructura predeterminada
        return {"Trabajadores": [], "Productos": [], "Ventas": [], "Inventario": []}
    except json.JSONDecodeError:
        # Si el archivo existe pero no es un JSON válido, se devuelve la estructura predeterminada
        return {"Trabajadores": [], "Productos": [], "Ventas": [], "Inventario": []}

# Función para guardar los datos en el archivo JSON
def guardar_datos(datos):
    try:
        with open("datos.json", "w") as archivo:
            json.dump(datos, archivo, indent=4)
    except IOError as e:
        print(f"Error al guardar los datos: {e}")



