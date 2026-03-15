# main.py
# OmniStock - Punto de entrada de la aplicación

"""
Sistema de Gestión de Inventario y Ventas.
Ejecutar este archivo para iniciar la aplicación de escritorio con Tkinter.
"""

import sys
from pathlib import Path

# Asegurar que el directorio del proyecto esté en el path
raiz = Path(__file__).resolve().parent
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))

from ui.login_view import LoginView
from ui.main_window import MainWindow


def main():
    """Muestra login; al validar, abre la ventana principal con el usuario."""
    def on_login_ok(usuario):
        app = MainWindow(usuario=usuario)
        app.run()

    login = LoginView(on_success=on_login_ok)
    login.run()


if __name__ == "__main__":
    main()
