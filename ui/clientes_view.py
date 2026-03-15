# ui/clientes_view.py
# OmniStock - Vista CRUD de clientes

"""
Interfaz del módulo de clientes: tabla, búsqueda y formulario CRUD.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from services.clientes_service import ClientesService


class ClientesView(ttk.Frame):
    """Frame con listado de clientes, búsqueda y formulario CRUD."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._construir_ui()

    def _construir_ui(self):
        f_busqueda = ttk.Frame(self)
        f_busqueda.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(f_busqueda, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        self.var_busqueda = tk.StringVar()
        self.entry_busqueda = ttk.Entry(f_busqueda, textvariable=self.var_busqueda, width=30)
        self.entry_busqueda.pack(side=tk.LEFT, padx=5)
        self.entry_busqueda.bind("<KeyRelease>", lambda e: self._refrescar_lista())
        ttk.Button(f_busqueda, text="Buscar", command=self._refrescar_lista).pack(side=tk.LEFT, padx=5)
        ttk.Button(f_busqueda, text="Limpiar", command=self._limpiar_busqueda).pack(side=tk.LEFT)

        f_contenido = ttk.Frame(self)
        f_contenido.pack(fill=tk.BOTH, expand=True)

        f_tabla = ttk.Frame(f_contenido)
        f_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        columnas = ("id", "nombre", "documento", "telefono", "email")
        self.tree = ttk.Treeview(f_tabla, columns=columnas, show="headings", height=14, selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("documento", text="Documento")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("email", text="Email")
        self.tree.column("id", width=50)
        self.tree.column("nombre", width=160)
        self.tree.column("documento", width=100)
        self.tree.column("telefono", width=100)
        self.tree.column("email", width=180)
        scroll = ttk.Scrollbar(f_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", lambda e: self._al_seleccionar())

        f_form = ttk.LabelFrame(f_contenido, text="Datos del cliente", padding=10)
        f_form.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        grid_f = ttk.Frame(f_form)
        grid_f.pack(fill=tk.X)
        ttk.Label(grid_f, text="Nombre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_nombre = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_nombre, width=28).grid(row=0, column=1, padx=5, pady=3)
        ttk.Label(grid_f, text="Documento:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_documento = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_documento, width=28).grid(row=1, column=1, padx=5, pady=3)
        ttk.Label(grid_f, text="Teléfono:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_telefono = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_telefono, width=28).grid(row=2, column=1, padx=5, pady=3)
        ttk.Label(grid_f, text="Email:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_email = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_email, width=28).grid(row=3, column=1, padx=5, pady=3)
        ttk.Label(grid_f, text="Dirección:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_direccion = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_direccion, width=28).grid(row=4, column=1, padx=5, pady=3)
        f_btn = ttk.Frame(f_form)
        f_btn.pack(fill=tk.X, pady=10)
        ttk.Button(f_btn, text="Nuevo", command=self._nuevo).pack(side=tk.LEFT, padx=3)
        ttk.Button(f_btn, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=3)
        ttk.Button(f_btn, text="Actualizar", command=self._actualizar).pack(side=tk.LEFT, padx=3)
        ttk.Button(f_btn, text="Eliminar", command=self._eliminar).pack(side=tk.LEFT, padx=3)
        self.id_seleccionado = None
        self._refrescar_lista()

    def refrescar_lista(self):
        self._refrescar_lista()

    def _refrescar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        texto = self.var_busqueda.get().strip()
        lista = ClientesService.buscar_por_texto(texto) if texto else ClientesService.listar_todos()
        for c in lista:
            self.tree.insert("", tk.END, values=(
                c.id, c.nombre, c.documento or "", c.telefono or "", c.email or ""
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
            self.var_documento.set(vals[2] if len(vals) > 2 else "")
            self.var_telefono.set(vals[3] if len(vals) > 3 else "")
            self.var_email.set(vals[4] if len(vals) > 4 else "")
            cli = ClientesService.buscar_por_id(self.id_seleccionado)
            self.var_direccion.set(cli.direccion or "" if cli else "")

    def _limpiar_formulario(self):
        self.id_seleccionado = None
        self.var_nombre.set("")
        self.var_documento.set("")
        self.var_telefono.set("")
        self.var_email.set("")
        self.var_direccion.set("")
        for s in self.tree.selection():
            self.tree.selection_remove(s)

    def _nuevo(self):
        self._limpiar_formulario()

    def _guardar(self):
        nombre = self.var_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del cliente no puede estar vacío.")
            return
        exito, msg = ClientesService.agregar(
            nombre,
            self.var_documento.get(),
            self.var_telefono.get(),
            self.var_email.get(),
            self.var_direccion.get(),
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._limpiar_formulario()
            self._refrescar_lista()
        else:
            messagebox.showerror("Error", msg)

    def _actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un cliente de la lista.")
            return
        nombre = self.var_nombre.get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre del cliente no puede estar vacío.")
            return
        exito, msg = ClientesService.editar(
            self.id_seleccionado, nombre,
            self.var_documento.get(), self.var_telefono.get(),
            self.var_email.get(), self.var_direccion.get(),
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._limpiar_formulario()
            self._refrescar_lista()
        else:
            messagebox.showerror("Error", msg)

    def _eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un cliente de la lista.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar este cliente?"):
            return
        exito, msg = ClientesService.eliminar(self.id_seleccionado)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._limpiar_formulario()
            self._refrescar_lista()
        else:
            messagebox.showerror("Error", msg)
