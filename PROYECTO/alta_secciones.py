import tkinter as tk
from tkinter import ttk, messagebox
from data import cargar_datos, guardar_datos

# Cargar los datos desde el archivo
datos = cargar_datos()

# Función para mostrar el formulario de alta o edición
def mostrar_formulario(seccion, tabla, item_seleccionado=None):
    def guardar_datos_formulario():
        entrada_valores = {campo: entradas[campo].get() for campo in campos}
        if any(valor.strip() == "" for valor in entrada_valores.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        # Si estamos en "Productos", agregar o actualizar el producto
        if seccion == "Productos":
            nombre_producto = entrada_valores["Nombre"]
            categoria_producto = entrada_valores["Categoría"]
            precio_producto = entrada_valores["Precio"]
            # Actualizar el producto si ya existe
            if item_seleccionado:
                for producto in datos["Productos"]:
                    if producto["Nombre"] == item_seleccionado["Nombre"]:
                        producto["Nombre"] = nombre_producto
                        producto["Categoría"] = categoria_producto
                        producto["Precio"] = precio_producto
                        break
            else:
                datos["Productos"].append({
                    "Nombre": nombre_producto,
                    "Categoría": categoria_producto,
                    "Precio": precio_producto
                })
                # También agregarlo en la sección de "Inventario"
                datos["Inventario"].append({
                    "Producto": nombre_producto,
                    "Cantidad Existente": 100,  # Se puede cambiar la cantidad inicial
                    "Cantidad Salida": 0
                })

        # Si estamos en "Trabajadores", agregar o actualizar el trabajador
        elif seccion == "Trabajadores":
            nombre_trabajador = entrada_valores["Nombre"]
            cargo_trabajador = entrada_valores["Cargo"]
            salario_trabajador = entrada_valores["Salario"]
            if item_seleccionado:
                for trabajador in datos["Trabajadores"]:
                    if trabajador["Nombre"] == item_seleccionado["Nombre"]:
                        trabajador["Nombre"] = nombre_trabajador
                        trabajador["Cargo"] = cargo_trabajador
                        trabajador["Salario"] = salario_trabajador
                        break
            else:
                datos["Trabajadores"].append({
                    "Nombre": nombre_trabajador,
                    "Cargo": cargo_trabajador,
                    "Salario": salario_trabajador
                })

        # Guardar los cambios en el archivo JSON
        guardar_datos(datos)  
        messagebox.showinfo("Éxito", f"{seccion[:-1]} guardado correctamente.")
        actualizar_tabla(tabla, seccion)  # Actualiza la tabla para reflejar los nuevos datos
        formulario.destroy()

    campos_por_seccion = {
        "Trabajadores": ["Nombre", "Cargo", "Salario"],
        "Productos": ["Nombre", "Categoría", "Precio"],
        "Consumo": ["Tipo (Domicilio/Mesa)", "Producto", "Cantidad", "Total"],  # Se agrega Total al Consumo
        "Proveedores": ["Nombre", "Producto", "Teléfono"],
        "Clientes": ["Nombre", "Domicilio", "Teléfono", "Referencia", "Producto"],
        "Ventas": ["Fecha", "Mesa/Domicilio", "Producto", "Cantidad Vendida", "Precio Total"],
        "Inventario": ["Producto", "Cantidad Existente", "Cantidad Salida"],
    }
    campos = campos_por_seccion[seccion]

    formulario = tk.Toplevel()
    formulario.title(f"Dar de Alta/Editar - {seccion}")
    formulario.geometry("400x400")

    entradas = {}
    for campo in campos:
        tk.Label(formulario, text=campo).pack(pady=5)
        entrada = tk.Entry(formulario)
        entrada.pack(pady=5)
        entradas[campo] = entrada

        # Si se está editando, precargar los valores existentes
        if item_seleccionado:
            if campo == "Nombre" and "Nombre" in item_seleccionado:
                entradas[campo].insert(0, item_seleccionado[campo])
            elif campo == "Categoría" and "Categoría" in item_seleccionado:
                entradas[campo].insert(0, item_seleccionado[campo])
            elif campo == "Precio" and "Precio" in item_seleccionado:
                entradas[campo].insert(0, item_seleccionado[campo])
            elif campo == "Cargo" and "Cargo" in item_seleccionado:
                entradas[campo].insert(0, item_seleccionado[campo])
            elif campo == "Salario" and "Salario" in item_seleccionado:
                entradas[campo].insert(0, item_seleccionado[campo])

    tk.Button(formulario, text="Guardar", command=guardar_datos_formulario).pack(pady=20)

# Función para actualizar la tabla en cada sección
def actualizar_tabla(tabla, seccion):
    # Limpiar tabla
    for item in tabla.get_children():
        tabla.delete(item)

    # Configurar las columnas de acuerdo con la sección
    if seccion == "Trabajadores":
        tabla["columns"] = ["Nombre", "Cargo", "Salario"]
    elif seccion == "Productos":
        tabla["columns"] = ["Nombre", "Categoría", "Precio"]
    elif seccion == "Consumo":
        tabla["columns"] = ["Tipo", "Producto", "Cantidad", "Total"]
    elif seccion == "Proveedores":
        tabla["columns"] = ["Nombre", "Producto", "Teléfono"]
    elif seccion == "Clientes":
        tabla["columns"] = ["Nombre", "Domicilio", "Teléfono", "Referencia", "Producto"]
    elif seccion == "Ventas":
        tabla["columns"] = ["Fecha", "Mesa/Domicilio", "Producto", "Cantidad Vendida", "Precio Total"]
    elif seccion == "Inventario":
        tabla["columns"] = ["Producto", "Cantidad Existente", "Cantidad Salida"]

    # Insertar los nuevos datos
    for registro in datos[seccion]:
        tabla.insert("", "end", values=tuple(registro.values()))

# Función para eliminar un dato
def eliminar_dato(tabla, seccion):
    # Obtener el item seleccionado
    item_seleccionado = tabla.selection()
    if not item_seleccionado:
        messagebox.showerror("Error", "Debe seleccionar un dato para eliminar.")
        return

    # Confirmar eliminación
    confirmacion = messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de eliminar este dato?")
    if confirmacion:
        item = item_seleccionado[0]
        valores_item = tabla.item(item, "values")
        
        # Eliminar el dato de la lista
        for registro in datos[seccion]:
            if tuple(registro.values()) == valores_item:
                datos[seccion].remove(registro)
                break
        
        # Guardar los cambios en el archivo JSON
        guardar_datos(datos)
        
        # Actualizar la tabla para reflejar la eliminación
        actualizar_tabla(tabla, seccion)
        messagebox.showinfo("Éxito", f"Dato eliminado de la sección {seccion}.")
        
# Función para mostrar productos con precios en la sección de Consumo
def mostrar_consumo(tabla, tipo_consumo):
    # Limpiar la tabla
    for item in tabla.get_children():
        tabla.delete(item)

    # Mostrar productos con precio
    productos_disponibles = [
        producto for producto in datos["Productos"]
        if any(item["Producto"] == producto["Nombre"] and item["Cantidad Existente"] > 0 for item in datos["Inventario"])
    ]

    # Crear una lista de productos para seleccionar
    productos_nombres = [producto["Nombre"] for producto in productos_disponibles]
    selected_product = tk.StringVar()
    
    # Crear un combobox para seleccionar el producto
    combobox_producto = ttk.Combobox(tabla, values=productos_nombres, textvariable=selected_product)
    combobox_producto.pack(pady=10)
    
    # Campo para ingresar la cantidad
    tk.Label(tabla, text="Cantidad:").pack(pady=5)
    cantidad_entrada = tk.Entry(tabla)
    cantidad_entrada.pack(pady=5)

    # Botón para realizar la venta
    def realizar_venta():
        producto_seleccionado = selected_product.get()
        if not producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return
        
        cantidad = int(cantidad_entrada.get())
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor que cero.")
            return
        
        # Buscar el precio del producto seleccionado
        precio = next((p["Precio"] for p in datos["Productos"] if p["Nombre"] == producto_seleccionado), 0)
        total = cantidad * precio

        # Actualizar inventario y registrar venta
        for inventario_item in datos["Inventario"]:
            if inventario_item["Producto"] == producto_seleccionado:
                inventario_item["Cantidad Existente"] -= cantidad
                inventario_item["Cantidad Salida"] += cantidad
                break

        # Registrar la venta
        fecha = "2024-12-03"  # Fecha de ejemplo
        datos["Ventas"].append({
            "Fecha": fecha,
            "Mesa/Domicilio": tipo_consumo,
            "Producto": producto_seleccionado,
            "Cantidad Vendida": cantidad,
            "Precio Total": total
        })

        # Guardar los cambios
        guardar_datos(datos)
        
        # Actualizar la tabla de consumo
        actualizar_tabla(tabla, "Ventas")
        messagebox.showinfo("Venta Realizada", "Venta realizada correctamente.")

    tk.Button(tabla, text="Realizar Venta", command=realizar_venta).pack(pady=10)

# Función para mostrar la ventana principal
def mostrar_ventana_principal(usuario):
    ventana_principal = tk.Tk()
    ventana_principal.title("Gestión de Restaurante")
    
    pestañas = ttk.Notebook(ventana_principal)
    secciones = ["Consumo", "Productos", "Trabajadores", "Proveedores", "Clientes", "Ventas", "Inventario"]

    for seccion in secciones:
        tab = tk.Frame(pestañas)
        pestañas.add(tab, text=seccion)
        
        tabla = ttk.Treeview(tab)
        tabla.pack(expand=True, fill=tk.BOTH)

        # Botón para dar de alta
        tk.Button(tab, text=f"Dar de alta {seccion[:-1]}", command=lambda seccion=seccion: mostrar_formulario(seccion, tabla)).pack(pady=5)
        
        # Botón para eliminar dato
        tk.Button(tab, text=f"Eliminar {seccion[:-1]}", command=lambda seccion=seccion: eliminar_dato(tabla, seccion)).pack(pady=5)
        
        # Inicializar consumo si es la sección de consumo
        if seccion == "Consumo":
            mostrar_consumo(tabla, "Mesa")
        else:
            actualizar_tabla(tabla, seccion)

        # Botón para actualizar la tabla
        tk.Button(tab, text=f"Actualizar {seccion}", command=lambda t=tabla, s=seccion: actualizar_tabla(t, s)).pack(pady=5)

        # Botón para eliminar datos seleccionados
        tk.Button(tab, text=f"Eliminar dato de {seccion}", command=lambda t=tabla, s=seccion: eliminar_dato(t, s)).pack(pady=5)

        # Botón para dar de alta en las secciones correspondientes
        if seccion in ["Trabajadores", "Productos", "Proveedores", "Clientes"]:
            tk.Button(tab, text=f"Dar de Alta en {seccion}", command=lambda s=seccion, t=tabla: mostrar_formulario(s, t)).pack(pady=5)

    pestañas.pack(expand=1, fill="both")
    ventana_principal.mainloop()

# Ejecutar el programa con un usuario
mostrar_ventana_principal("Usuario")