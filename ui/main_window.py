# ui/main_window.py
# OmniStock - Ventana principal de la aplicación

"""
Ventana principal con pestañas: Productos y Ventas.
Contiene el menú o navegación entre módulos.
"""

import tkinter as tk
from tkinter import ttk

from ui.productos_view import ProductosView
from ui.ventas_view import VentasView


class MainWindow:
    """Ventana principal con notebook (pestañas) para Productos y Ventas."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OmniStock - Gestión de Inventario y Ventas")
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        # Estilo
        style = ttk.Style()
        style.theme_use("clam")

        # Contenedor principal: pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pestaña Productos
        self.frame_productos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_productos, text="  Productos  ")
        self.productos_view = ProductosView(self.frame_productos)
        self.productos_view.pack(fill=tk.BOTH, expand=True)

        # Pestaña Ventas
        self.frame_ventas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_ventas, text="  Ventas  ")
        self.ventas_view = VentasView(self.frame_ventas, on_venta_registrada=self._refrescar_productos)
        self.ventas_view.pack(fill=tk.BOTH, expand=True)

        # Al cambiar a la pestaña Productos, refrescar la lista para ver stock actualizado
        self.notebook.bind("<<NotebookTabChanged>>", self._al_cambiar_pestana)

    def _al_cambiar_pestana(self, event=None):
        """Cuando el usuario cambia a la pestaña Productos, refrescar la lista."""
        try:
            if self.notebook.index(self.notebook.select()) == 0:
                self.productos_view.refrescar_lista()
        except (tk.TclError, AttributeError):
            pass

    def _refrescar_productos(self):
        """Llamado después de registrar una venta para actualizar la lista de productos (stock)."""
        self.productos_view.refrescar_lista()

    def run(self):
        """Inicia el bucle principal de la aplicación."""
        self.root.mainloop()
