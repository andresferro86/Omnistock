# ui/productos_view.py
# OmniStock - Vista de productos (listar, agregar, editar, eliminar, buscar)

"""
Interfaz del módulo de productos: tabla, formulario y botones.
Delega en InventarioService para todas las operaciones.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from services.inventario_service import InventarioService
from utils.helpers import validar_decimal_positivo, validar_entero_positivo, formatear_precio


class ProductosView(ttk.Frame):
    """Frame con listado de productos, búsqueda y formulario CRUD."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._construir_ui()

    def _construir_ui(self):
        # --- Búsqueda (arriba) ---
        f_busqueda = ttk.Frame(self)
        f_busqueda.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(f_busqueda, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.var_busqueda = tk.StringVar()
        self.entry_busqueda = ttk.Entry(f_busqueda, textvariable=self.var_busqueda, width=30)
        self.entry_busqueda.pack(side=tk.LEFT, padx=5)
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self._refrescar_lista())
        ttk.Button(f_busqueda, text="Buscar", command=self._refrescar_lista).pack(side=tk.LEFT, padx=5)
        ttk.Button(f_busqueda, text="Limpiar", command=self._limpiar_busqueda).pack(side=tk.LEFT)

        # --- Contenedor: tabla a la izquierda, formulario a la derecha ---
        f_contenido = ttk.Frame(self)
        f_contenido.pack(fill=tk.BOTH, expand=True)

        # --- Tabla (izquierda) ---
        f_tabla = ttk.Frame(f_contenido)
        f_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        columnas = ("id", "nombre", "descripcion", "precio", "stock")
        self.tree = ttk.Treeview(f_tabla, columns=columnas, show="headings", height=14, selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")
        self.tree.column("id", width=50)
        self.tree.column("nombre", width=180)
        self.tree.column("descripcion", width=220)
        self.tree.column("precio", width=100)
        self.tree.column("stock", width=60)
        scroll = ttk.Scrollbar(f_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", lambda e: self._al_seleccionar())

        # --- Panel "Datos del producto" (derecha) ---
        f_form = ttk.LabelFrame(f_contenido, text="Datos del producto", padding=10)
        f_form.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        grid_f = ttk.Frame(f_form)
        grid_f.pack(fill=tk.X)
        ttk.Label(grid_f, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_nombre = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_nombre, width=28).grid(row=0, column=1, padx=5, pady=3)
        ttk.Label(grid_f, text="Descripción:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_descripcion = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_descripcion, width=28).grid(row=1, column=1, padx=5, pady=3)
        ttk.Label(grid_f, text="Precio:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_precio = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_precio, width=12).grid(row=2, column=1, sticky=tk.W, padx=5, pady=3)
        ttk.Label(grid_f, text="Stock:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_stock = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_stock, width=12).grid(row=3, column=1, sticky=tk.W, padx=5, pady=3)

        f_btn = ttk.Frame(f_form)
        f_btn.pack(fill=tk.X, pady=10)
        ttk.Button(f_btn, text="Nuevo", command=self._nuevo).pack(side=tk.LEFT, padx=3)
        ttk.Button(f_btn, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=3)
        ttk.Button(f_btn, text="Actualizar", command=self._actualizar).pack(side=tk.LEFT, padx=3)
        ttk.Button(f_btn, text="Eliminar", command=self._eliminar).pack(side=tk.LEFT, padx=3)

        self.id_seleccionado = None
        self._refrescar_lista()

    def refrescar_lista(self):
        """Refresca la lista desde la BD (público para llamar desde main_window o ventas)."""
        self._refrescar_lista()

    def _refrescar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        texto = self.var_busqueda.get().strip()
        if texto:
            productos = InventarioService.buscar_por_texto(texto)
        else:
            productos = InventarioService.listar_todos()
        for p in productos:
            self.tree.insert("", tk.END, values=(
                p.id,
                p.nombre,
                p.descripcion or "",
                formatear_precio(p.precio),
                p.stock,
            ))

    def _limpiar_busqueda(self):
        self.var_busqueda.set("")
        self._refrescar_lista()

    def _al_seleccionar(self):
        sel = self.tree.selection()
        if not sel:
            self.id_seleccionado = None
            return
        item = self.tree.item(sel[0])
        vals = item["values"]
        if vals:
            self.id_seleccionado = int(vals[0])
            self.var_nombre.set(vals[1])
            self.var_descripcion.set(vals[2] or "")
            self.var_precio.set(vals[3] if len(vals) > 3 else "")
            self.var_stock.set(str(vals[4]) if len(vals) > 4 else "")

    def _limpiar_formulario(self):
        self.id_seleccionado = None
        self.var_nombre.set("")
        self.var_descripcion.set("")
        self.var_precio.set("")
        self.var_stock.set("")
        self.tree.selection_remove(self.tree.selection())

    def _nuevo(self):
        self._limpiar_formulario()

    def _guardar(self):
        nombre = self.var_nombre.get().strip()
        ok_precio, precio, msg_p = validar_decimal_positivo(self.var_precio.get(), "El precio")
        ok_stock, stock, msg_s = validar_entero_positivo(self.var_stock.get(), "El stock")
        if not nombre:
            messagebox.showerror("Error", "El nombre del producto no puede estar vacío.")
            return
        if not ok_precio:
            messagebox.showerror("Error", msg_p)
            return
        if not ok_stock:
            messagebox.showerror("Error", msg_s)
            return
        exito, mensaje = InventarioService.agregar(
            nombre, precio, stock, self.var_descripcion.get()
        )
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self._limpiar_formulario()
            self._refrescar_lista()
        else:
            messagebox.showerror("Error", mensaje)

    def _actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un producto de la lista para actualizar.")
            return
        nombre = self.var_nombre.get().strip()
        ok_precio, precio, msg_p = validar_decimal_positivo(self.var_precio.get(), "El precio")
        ok_stock, stock, msg_s = validar_entero_positivo(self.var_stock.get(), "El stock")
        if not nombre:
            messagebox.showerror("Error", "El nombre del producto no puede estar vacío.")
            return
        if not ok_precio:
            messagebox.showerror("Error", msg_p)
            return
        if not ok_stock:
            messagebox.showerror("Error", msg_s)
            return
        exito, mensaje = InventarioService.editar(
            self.id_seleccionado, nombre, precio, stock, self.var_descripcion.get()
        )
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self._limpiar_formulario()
            self._refrescar_lista()
        else:
            messagebox.showerror("Error", mensaje)

    def _eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un producto de la lista para eliminar.")
            return
        if not messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            return
        exito, mensaje = InventarioService.eliminar(self.id_seleccionado)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self._limpiar_formulario()
            self._refrescar_lista()
        else:
            messagebox.showerror("Error", mensaje)
