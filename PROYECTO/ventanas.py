import tkinter as tk
from tkinter import ttk

def mostrar_ventana_principal():
    ventana_principal = tk.Tk()
    ventana_principal.title("Sistema de Gestión")
    ventana_principal.geometry("800x600")

    pestañas = ttk.Notebook(ventana_principal)

    # Secciones
    for seccion in ["Trabajadores", "Productos", "Consumo", "Proveedores", "Clientes", "Ventas", "Inventario"]:
        tab = ttk.Frame(pestañas)
        pestañas.add(tab, text=seccion)
        tk.Label(tab, text=f"Sección de {seccion}").pack(pady=10)

    pestañas.pack(expand=1, fill="both")
    ventana_principal.mainloop()