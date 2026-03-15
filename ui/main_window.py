# ui/main_window.py
# OmniStock - Ventana principal (pestañas según rol: Admin o Empleado/Vendedor)

import tkinter as tk
from tkinter import ttk

from ui.productos_view import ProductosView
from ui.clientes_view import ClientesView
from ui.ventas_view import VentasView
from ui.usuarios_view import UsuariosView


class MainWindow:
    """Ventana principal. Administrador: Productos, Clientes, Ventas, Usuarios. Vendedor/Empleado: Productos (solo ver stock), Clientes, Ventas."""

    def __init__(self, usuario=None):
        self.usuario = usuario
        self.root = tk.Tk()
        titulo = "OmniStock - Gestión de Inventario y Ventas"
        if usuario:
            titulo += f"  —  Usuario: {usuario.usuario} ({usuario.nombre_rol})"
        self.root.title(titulo)
        self.root.geometry("900x600")
        self.root.minsize(800, 500)

        style = ttk.Style()
        style.theme_use("clam")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        es_admin = usuario and usuario.nombre_rol == "Administrador"
        # Empleado/Vendedor: solo ver stock en Productos (sin editar), Clientes (crear/ver), Ventas
        solo_lectura_productos = not es_admin

        # Pestaña Productos (lectura completa para Admin, solo consulta stock para Empleado)
        self.frame_productos = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_productos, text="  Productos  " if es_admin else "  Stock  ")
        self.productos_view = ProductosView(self.frame_productos, solo_lectura=solo_lectura_productos)
        self.productos_view.pack(fill=tk.BOTH, expand=True)

        # Pestaña Clientes
        self.frame_clientes = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_clientes, text="  Clientes  ")
        self.clientes_view = ClientesView(self.frame_clientes)
        self.clientes_view.pack(fill=tk.BOTH, expand=True)

        # Pestaña Ventas
        self.frame_ventas = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.frame_ventas, text="  Ventas  ")
        self.ventas_view = VentasView(
            self.frame_ventas,
            on_venta_registrada=self._refrescar_productos,
            on_refrescar_clientes=self._refrescar_clientes,
        )
        self.ventas_view.pack(fill=tk.BOTH, expand=True)

        # Pestaña Usuarios (solo Administrador)
        self.usuarios_view = None
        if es_admin:
            self.frame_usuarios = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(self.frame_usuarios, text="  Usuarios  ")
            self.usuarios_view = UsuariosView(self.frame_usuarios)
            self.usuarios_view.pack(fill=tk.BOTH, expand=True)

        self.notebook.bind("<<NotebookTabChanged>>", self._al_cambiar_pestana)

    def _al_cambiar_pestana(self, event=None):
        try:
            idx = self.notebook.index(self.notebook.select())
            if idx == 0:
                self.productos_view.refrescar_lista()
            elif idx == 1:
                self.clientes_view.refrescar_lista()
            elif self.usuarios_view and idx == 3:
                self.usuarios_view.refrescar_lista()
        except (tk.TclError, AttributeError):
            pass

    def _refrescar_productos(self):
        self.productos_view.refrescar_lista()

    def _refrescar_clientes(self):
        self.clientes_view.refrescar_lista()

    def run(self):
        self.root.mainloop()
