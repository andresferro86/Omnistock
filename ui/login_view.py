# ui/login_view.py
# OmniStock - Ventana de inicio de sesión

"""
Ventana de login. Al validar usuario y contraseña con AuthService,
notifica al callback con el Usuario y cierra la ventana.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from services.auth_service import AuthService
from models.usuario import Usuario


class LoginView:
    """Ventana modal de login. Al éxito llama a on_success(usuario)."""

    def __init__(self, on_success):
        """
        on_success: callback(usuario: Usuario) cuando el login es correcto.
        """
        self.on_success = on_success
        self.root = tk.Tk()
        self.root.title("OmniStock - Iniciar sesión")
        self.root.geometry("320x180")
        self.root.resizable(False, False)
        self._construir_ui()

    def _construir_ui(self):
        f = ttk.Frame(self.root, padding=20)
        f.pack(fill=tk.BOTH, expand=True)
        ttk.Label(f, text="Usuario:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=8)
        self.var_usuario = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_usuario, width=25).grid(row=0, column=1, padx=5, pady=8)
        ttk.Label(f, text="Contraseña:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=8)
        self.var_password = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_password, width=25, show="*").grid(row=1, column=1, padx=5, pady=8)
        btn_f = ttk.Frame(f)
        btn_f.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(btn_f, text="Iniciar sesión", command=self._login).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_f, text="Salir", command=self.root.quit).pack(side=tk.LEFT)
        self.var_usuario.set("admin")
        self.var_password.set("admin")

    def _login(self):
        usuario = self.var_usuario.get().strip()
        password = self.var_password.get()
        if not usuario:
            messagebox.showwarning("Aviso", "Ingrese el usuario.")
            return
        ok, user, msg = AuthService.login(usuario, password)
        if ok and user:
            self.root.destroy()  # Cerrar primero la ventana de login
            self.on_success(user)  # Luego abrir la ventana principal (mainloop bloquea aquí)
        else:
            messagebox.showerror("Error de acceso", msg)

    def run(self):
        self.root.mainloop()
