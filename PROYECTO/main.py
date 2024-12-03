from login import iniciar_sesion
from alta_secciones import mostrar_ventana_principal

if __name__ == "__main__":
    usuario = iniciar_sesion()
    if usuario:  # Si el inicio de sesión es exitoso
        mostrar_ventana_principal(usuario)
