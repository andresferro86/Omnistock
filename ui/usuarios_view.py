# ui/usuarios_view.py
# OmniStock - Vista CRUD de usuarios (solo Administrador)

import tkinter as tk
from tkinter import ttk, messagebox

from services.usuarios_service import UsuariosService


class UsuariosView(ttk.Frame):
    """Frame con listado de usuarios y formulario CRUD."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._construir_ui()

    def _construir_ui(self):
        f_tabla = ttk.Frame(self)
        f_tabla.pack(fill=tk.BOTH, expand=True)
        columnas = ("id", "usuario", "rol", "nombre_completo", "activo")
        self.tree = ttk.Treeview(f_tabla, columns=columnas, show="headings", height=12, selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("rol", text="Rol")
        self.tree.heading("nombre_completo", text="Nombre completo")
        self.tree.heading("activo", text="Activo")
        self.tree.column("id", width=50)
        self.tree.column("usuario", width=120)
        self.tree.column("rol", width=120)
        self.tree.column("nombre_completo", width=200)
        self.tree.column("activo", width=60)
        scroll = ttk.Scrollbar(f_tabla, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<<TreeviewSelect>>", lambda e: self._al_seleccionar())

        f_form = ttk.LabelFrame(self, text="Datos del usuario", padding=10)
        f_form.pack(fill=tk.X, pady=10)
        grid_f = ttk.Frame(f_form)
        grid_f.pack(fill=tk.X)
        ttk.Label(grid_f, text="Usuario (login):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_usuario = tk.StringVar()
        self.entry_usuario = ttk.Entry(grid_f, textvariable=self.var_usuario, width=25)
        self.entry_usuario.grid(row=0, column=1, padx=5, pady=3)
        ttk.Label(grid_f, text="Contraseña (dejar en blanco para no cambiar):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_password = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_password, width=25, show="*").grid(row=1, column=1, padx=5, pady=3)
        ttk.Label(grid_f, text="Rol:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_rol = tk.StringVar()
        self.combo_rol = ttk.Combobox(grid_f, textvariable=self.var_rol, width=22, state="readonly")
        self.combo_rol.grid(row=2, column=1, sticky=tk.W, padx=5, pady=3)
        ttk.Label(grid_f, text="Nombre completo:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=3)
        self.var_nombre = tk.StringVar()
        ttk.Entry(grid_f, textvariable=self.var_nombre, width=25).grid(row=3, column=1, padx=5, pady=3)
        self.var_activo = tk.BooleanVar(value=True)
        ttk.Checkbutton(grid_f, text="Activo", variable=self.var_activo).grid(row=4, column=1, sticky=tk.W, padx=5, pady=3)
        f_btn = ttk.Frame(f_form)
        f_btn.pack(fill=tk.X, pady=10)
        ttk.Button(f_btn, text="Nuevo", command=self._nuevo).pack(side=tk.LEFT, padx=3)
        ttk.Button(f_btn, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=3)
        ttk.Button(f_btn, text="Actualizar", command=self._actualizar).pack(side=tk.LEFT, padx=3)
        ttk.Button(f_btn, text="Eliminar", command=self._eliminar).pack(side=tk.LEFT, padx=3)
        self.id_seleccionado = None
        self._cargar_roles()
        self._refrescar_lista()

    def _cargar_roles(self):
        roles = UsuariosService.listar_roles()
        self.lista_roles = roles
        self.combo_rol["values"] = [r[1] for r in roles]
        if roles:
            self.combo_rol.current(0)

    def refrescar_lista(self):
        self._refrescar_lista()

    def _refrescar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for u in UsuariosService.listar_todos():
            self.tree.insert("", tk.END, values=(u.id, u.usuario, u.nombre_rol, u.nombre_completo or "", "Sí" if u.activo else "No"))

    def _al_seleccionar(self):
        sel = self.tree.selection()
        if not sel:
            self.id_seleccionado = None
            return
        item = self.tree.item(sel[0])
        vals = item["values"]
        if vals:
            self.id_seleccionado = int(vals[0])
            self.var_usuario.set(vals[1])
            self.var_password.set("")
            rol_name = vals[2] if len(vals) > 2 else ""
            for i, (_, n) in enumerate(self.lista_roles):
                if n == rol_name:
                    self.combo_rol.current(i)
                    break
            self.var_nombre.set(vals[3] if len(vals) > 3 else "")
            u = UsuariosService.buscar_por_id(self.id_seleccionado)
            self.var_activo.set(u.activo if u else True)
            self.entry_usuario.config(state="disabled")

    def _nuevo(self):
        self.id_seleccionado = None
        self.var_usuario.set("")
        self.var_password.set("")
        self.var_nombre.set("")
        self.var_activo.set(True)
        self.entry_usuario.config(state="normal")
        if self.lista_roles:
            self.combo_rol.current(0)
        for s in self.tree.selection():
            self.tree.selection_remove(s)

    def _guardar(self):
        usuario = self.var_usuario.get().strip()
        password = self.var_password.get()
        if not usuario:
            messagebox.showerror("Error", "El usuario (login) no puede estar vacío.")
            return
        if not password:
            messagebox.showerror("Error", "Ingrese la contraseña para el nuevo usuario.")
            return
        idx = self.combo_rol.current()
        if idx < 0 or idx >= len(self.lista_roles):
            messagebox.showerror("Error", "Seleccione un rol.")
            return
        id_rol = self.lista_roles[idx][0]
        exito, msg = UsuariosService.agregar(usuario, password, id_rol, self.var_nombre.get())
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._nuevo()
            self._refrescar_lista()
        else:
            messagebox.showerror("Error", msg)

    def _actualizar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un usuario de la lista.")
            return
        idx = self.combo_rol.current()
        if idx < 0 or idx >= len(self.lista_roles):
            messagebox.showerror("Error", "Seleccione un rol.")
            return
        id_rol = self.lista_roles[idx][0]
        exito, msg = UsuariosService.editar(
            self.id_seleccionado,
            id_rol,
            self.var_nombre.get(),
            self.var_activo.get(),
            self.var_password.get().strip() or None,
        )
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.var_password.set("")
            self._refrescar_lista()
        else:
            messagebox.showerror("Error", msg)

    def _eliminar(self):
        if self.id_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un usuario de la lista.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            return
        exito, msg = UsuariosService.eliminar(self.id_seleccionado)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self._nuevo()
            self._refrescar_lista()
        else:
            messagebox.showerror("Error", msg)
