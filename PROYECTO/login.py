import tkinter as tk
from tkinter import messagebox
from data import USUARIOS

def iniciar_sesion():
    def validar_credenciales():
        username = entrada_usuario.get()
        password = entrada_contraseña.get()

        if username in USUARIOS and USUARIOS[username] == password:
            messagebox.showinfo("Inicio de Sesión", f"¡Bienvenido, {username}!")
            ventana_login.quit()  # Usamos `quit()` para salir del ciclo de mainloop y regresar el valor
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.geometry("300x200")

    tk.Label(ventana_login, text="Usuario:").pack(pady=5)
    entrada_usuario = tk.Entry(ventana_login)
    entrada_usuario.pack(pady=5)

    tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
    entrada_contraseña = tk.Entry(ventana_login, show="*")
    entrada_contraseña.pack(pady=5)

    tk.Button(ventana_login, text="Iniciar Sesión", command=validar_credenciales).pack(pady=20)

    ventana_login.mainloop()  # Mantén la ventana de login activa hasta que el usuario ingrese correctamente

    return entrada_usuario.get()  # Devuelve el nombre de usuario cuando se cierra correctamente la ventana
