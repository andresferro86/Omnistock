# ui/ventas_view.py
# OmniStock - Vista de ventas (registrar venta e historial)

"""
Interfaz del módulo de ventas: carrito de venta actual e historial.
Valida stock y cantidades antes de registrar.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal

from services.inventario_service import InventarioService
from services.ventas_service import VentasService
from utils.helpers import validar_entero_positivo, formatear_precio


# Tipo interno para una línea en el carrito: (id_producto, nombre, cantidad, precio_unitario)
LineaCarrito = tuple


class VentasView(ttk.Frame):
    """Frame con formulario de nueva venta y listado de historial."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.lineas_carrito = []  # List[Tuple[id_producto, nombre, cantidad, Decimal]]
        self._construir_ui()

    def _construir_ui(self):
        # --- Nueva venta ---
        f_venta = ttk.LabelFrame(self, text="Nueva venta", padding=10)
        f_venta.pack(fill=tk.BOTH, expand=True)

        # Producto y cantidad
        f_linea = ttk.Frame(f_venta)
        f_linea.pack(fill=tk.X)
        ttk.Label(f_linea, text="Producto:").pack(side=tk.LEFT, padx=(0, 5))
        self.var_producto = tk.StringVar()
        self.combo_productos = ttk.Combobox(f_linea, textvariable=self.var_producto, width=35, state="readonly")
        self.combo_productos.pack(side=tk.LEFT, padx=5)
        ttk.Label(f_linea, text="Cantidad:").pack(side=tk.LEFT, padx=(15, 5))
        self.var_cantidad = tk.StringVar(value="1")
        ttk.Entry(f_linea, textvariable=self.var_cantidad, width=8).pack(side=tk.LEFT, padx=5)
        ttk.Button(f_linea, text="Agregar a la venta", command=self._agregar_linea).pack(side=tk.LEFT, padx=10)

        # Lista de líneas de la venta actual
        ttk.Label(f_venta, text="Detalle de la venta:").pack(anchor=tk.W)
        columnas = ("producto", "cantidad", "precio_unit", "subtotal")
        self.tree_carrito = ttk.Treeview(f_venta, columns=columnas, show="headings", height=6)
        self.tree_carrito.heading("producto", text="Producto")
        self.tree_carrito.heading("cantidad", text="Cantidad")
        self.tree_carrito.heading("precio_unit", text="P. unitario")
        self.tree_carrito.heading("subtotal", text="Subtotal")
        for c in columnas:
            self.tree_carrito.column(c, width=120)
        self.tree_carrito.pack(fill=tk.X, pady=5)
        ttk.Button(f_venta, text="Quitar línea seleccionada", command=self._quitar_linea).pack(anchor=tk.W, pady=2)

        # Cliente y total
        f_tot = ttk.Frame(f_venta)
        f_tot.pack(fill=tk.X)
        ttk.Label(f_tot, text="Cliente (opcional):").pack(side=tk.LEFT, padx=(0, 5))
        self.var_cliente = tk.StringVar()
        ttk.Entry(f_tot, textvariable=self.var_cliente, width=30).pack(side=tk.LEFT, padx=5)
        self.lbl_total = ttk.Label(f_tot, text="Total: 0.00")
        self.lbl_total.pack(side=tk.RIGHT, padx=10)
        ttk.Button(f_venta, text="Registrar venta", command=self._registrar_venta).pack(pady=10)

        # --- Historial de ventas ---
        f_hist = ttk.LabelFrame(self, text="Historial de ventas", padding=10)
        f_hist.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Contenedor: tabla historial a la izquierda, detalle de venta a la derecha
        f_hist_contenido = ttk.Frame(f_hist)
        f_hist_contenido.pack(fill=tk.BOTH, expand=True)

        columnas_h = ("id", "fecha", "total", "cliente")
        self.tree_ventas = ttk.Treeview(f_hist_contenido, columns=columnas_h, show="headings", height=8)
        self.tree_ventas.heading("id", text="ID")
        self.tree_ventas.heading("fecha", text="Fecha")
        self.tree_ventas.heading("total", text="Total")
        self.tree_ventas.heading("cliente", text="Cliente")
        self.tree_ventas.column("id", width=50)
        self.tree_ventas.column("fecha", width=180)
        self.tree_ventas.column("total", width=80)
        self.tree_ventas.column("cliente", width=200)
        scroll_h = ttk.Scrollbar(f_hist_contenido, orient=tk.VERTICAL, command=self.tree_ventas.yview)
        self.tree_ventas.configure(yscrollcommand=scroll_h.set)
        self.tree_ventas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_h.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_ventas.bind("<<TreeviewSelect>>", lambda e: self._al_seleccionar_venta())

        # Panel "Detalle de la venta seleccionada"
        f_detalle = ttk.LabelFrame(f_hist_contenido, text="Detalle de la venta seleccionada", padding=10)
        f_detalle.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.lbl_fecha_venta = ttk.Label(f_detalle, text="Fecha y hora: —")
        self.lbl_fecha_venta.pack(anchor=tk.W)
        self.lbl_cliente_venta = ttk.Label(f_detalle, text="Cliente: —")
        self.lbl_cliente_venta.pack(anchor=tk.W)

        columnas_d = ("producto", "cantidad", "precio_unit", "subtotal")
        self.tree_detalle_venta = ttk.Treeview(f_detalle, columns=columnas_d, show="headings", height=6)
        self.tree_detalle_venta.heading("producto", text="Producto")
        self.tree_detalle_venta.heading("cantidad", text="Cantidad")
        self.tree_detalle_venta.heading("precio_unit", text="P. unitario")
        self.tree_detalle_venta.heading("subtotal", text="Subtotal")
        for c in columnas_d:
            self.tree_detalle_venta.column(c, width=100)
        self.tree_detalle_venta.pack(fill=tk.BOTH, expand=True, pady=5)
        self.lbl_total_venta = ttk.Label(f_detalle, text="Total: —")
        self.lbl_total_venta.pack(anchor=tk.E)

        ttk.Button(f_hist, text="Actualizar historial", command=self._refrescar_historial).pack(anchor=tk.W, pady=5)

        self.lista_ventas = []
        self._cargar_combo_productos()
        self._refrescar_historial()

    def _cargar_combo_productos(self):
        productos = InventarioService.listar_todos()
        self.lista_productos = productos
        opciones = [f"{p.id} - {p.nombre} (stock: {p.stock})" for p in productos]
        self.combo_productos["values"] = opciones
        if opciones:
            self.combo_productos.current(0)
        else:
            self.var_producto.set("")

    def _agregar_linea(self):
        idx = self.combo_productos.current()
        if idx < 0 or idx >= len(self.lista_productos):
            messagebox.showwarning("Aviso", "Seleccione un producto.")
            return
        producto = self.lista_productos[idx]
        ok, cantidad, msg = validar_entero_positivo(self.var_cantidad.get(), "Cantidad")
        if not ok or cantidad is None:
            messagebox.showerror("Error", msg)
            return
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor que cero.")
            return
        if not producto.tiene_stock_suficiente(cantidad):
            messagebox.showerror("Error", f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}.")
            return
        precio = Decimal(str(producto.precio))
        subtotal = cantidad * precio
        self.lineas_carrito.append((producto.id, producto.nombre, cantidad, precio))
        self.tree_carrito.insert("", tk.END, values=(
            producto.nombre, cantidad, formatear_precio(precio), formatear_precio(subtotal)
        ))
        self._actualizar_total()
        self.var_cantidad.set("1")

    def _quitar_linea(self):
        sel = self.tree_carrito.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione una línea para quitar.")
            return
        item = self.tree_carrito.item(sel[0])
        idx = self.tree_carrito.index(sel[0])
        self.tree_carrito.delete(sel[0])
        if 0 <= idx < len(self.lineas_carrito):
            self.lineas_carrito.pop(idx)
        self._actualizar_total()

    def _actualizar_total(self):
        total = sum(cant * float(precio) for _, _, cant, precio in self.lineas_carrito)
        self.lbl_total.config(text=f"Total: {formatear_precio(total)}")

    def _registrar_venta(self):
        if not self.lineas_carrito:
            messagebox.showwarning("Aviso", "Agregue al menos un producto a la venta.")
            return
        lineas = [(id_p, cant, precio) for id_p, _, cant, precio in self.lineas_carrito]
        exito, mensaje = VentasService.registrar_venta(
            lineas,
            cliente=self.var_cliente.get(),
            observaciones="",
        )
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self._limpiar_carrito()
            self._refrescar_historial()
            self._cargar_combo_productos()
        else:
            messagebox.showerror("Error", mensaje)

    def _limpiar_carrito(self):
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
        self.lineas_carrito.clear()
        self._actualizar_total()
        self.var_cliente.set("")

    def _refrescar_historial(self):
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)
        self.lista_ventas = VentasService.listar_ventas()
        for v in self.lista_ventas:
            self.tree_ventas.insert("", tk.END, values=(
                v.id,
                v.fecha_venta[:19] if len(v.fecha_venta) >= 19 else v.fecha_venta,
                formatear_precio(v.total),
                v.cliente or "",
            ))
        self._limpiar_detalle_venta()

    def _limpiar_detalle_venta(self):
        """Limpia el panel de detalle de la venta."""
        self.lbl_fecha_venta.config(text="Fecha y hora: —")
        self.lbl_cliente_venta.config(text="Cliente: —")
        self.lbl_total_venta.config(text="Total: —")
        for item in self.tree_detalle_venta.get_children():
            self.tree_detalle_venta.delete(item)

    def _al_seleccionar_venta(self):
        """Al hacer clic en una venta del historial, muestra su detalle (fecha, hora, ítems, total)."""
        sel = self.tree_ventas.selection()
        if not sel:
            self._limpiar_detalle_venta()
            return
        item = self.tree_ventas.item(sel[0])
        vals = item["values"]
        if not vals:
            self._limpiar_detalle_venta()
            return
        idx = self.tree_ventas.index(sel[0])
        if idx < 0 or idx >= len(self.lista_ventas):
            self._limpiar_detalle_venta()
            return
        v = self.lista_ventas[idx]
        # Fecha y hora de registro (mostrar completa)
        fecha_hora = v.fecha_venta if isinstance(v.fecha_venta, str) else str(v.fecha_venta)
        self.lbl_fecha_venta.config(text=f"Fecha y hora: {fecha_hora}")
        self.lbl_cliente_venta.config(text=f"Cliente: {v.cliente or '—'}")
        self.lbl_total_venta.config(text=f"Total: {formatear_precio(v.total)}")
        # Limpiar y llenar tabla de detalle
        for child in self.tree_detalle_venta.get_children():
            self.tree_detalle_venta.delete(child)
        for d in v.detalles:
            self.tree_detalle_venta.insert("", tk.END, values=(
                d.nombre_producto,
                d.cantidad,
                formatear_precio(d.precio_unitario),
                formatear_precio(d.subtotal),
            ))
