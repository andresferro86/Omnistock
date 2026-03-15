# services/auth_service.py
# OmniStock - Autenticación y gestión de usuarios

"""
Login, verificación de contraseña con hash (bcrypt) y creación de usuario admin por defecto.
Usa la librería bcrypt directamente para evitar incompatibilidades con passlib.
"""

from typing import Optional, Tuple

import bcrypt

from db.conexion import obtener_conexion, cerrar_conexion
from models.usuario import Usuario

# bcrypt limita la contraseña a 72 bytes
_MAX_PASSWORD_BYTES = 72


class AuthService:
    """Servicio de autenticación y usuarios."""

    @staticmethod
    def _hash_password(plain: str) -> str:
        """Genera el hash bcrypt de la contraseña (máx. 72 bytes)."""
        p = (plain or "").encode("utf-8")[: _MAX_PASSWORD_BYTES]
        return bcrypt.hashpw(p, bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(plain: str, password_hash: str) -> bool:
        """Verifica que la contraseña en texto plano coincida con el hash."""
        try:
            p = (plain or "").encode("utf-8")[: _MAX_PASSWORD_BYTES]
            h = (password_hash or "").encode("utf-8")
            return bcrypt.checkpw(p, h)
        except Exception:
            return False

    @staticmethod
    def ensure_admin_exists() -> None:
        """Si no existe ningún usuario, crea admin/admin (contraseña: admin)."""
        conn = obtener_conexion()
        if not conn:
            return
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) AS n FROM usuarios")
            row = cursor.fetchone()
            cursor.close()
            if row and row["n"] > 0:
                return
            cursor = conn.cursor()
            password_hash = AuthService._hash_password("admin")
            cursor.execute(
                "INSERT INTO usuarios (usuario, password_hash, id_rol, nombre_completo, activo) VALUES (%s, %s, 1, %s, 1)",
                ("admin", password_hash, "Administrador"),
            )
            conn.commit()
            cursor.close()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error al crear usuario admin: {e}")
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def login(usuario: str, password: str) -> Tuple[bool, Optional[Usuario], str]:
        """
        Intenta iniciar sesión. Crea admin/admin si no hay usuarios.
        Returns: (éxito, Usuario o None, mensaje)
        """
        AuthService.ensure_admin_exists()
        conn = obtener_conexion()
        if not conn:
            return False, None, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT u.id, u.usuario, u.password_hash, u.id_rol, u.nombre_completo, u.activo, r.nombre AS nombre_rol "
                "FROM usuarios u JOIN roles r ON u.id_rol = r.id WHERE u.usuario = %s",
                (usuario.strip(),),
            )
            row = cursor.fetchone()
            cursor.close()
            if not row:
                return False, None, "Usuario o contraseña incorrectos."
            if not row.get("activo", 1):
                return False, None, "Usuario desactivado."
            if not AuthService.verify_password(password, row["password_hash"]):
                return False, None, "Usuario o contraseña incorrectos."
            user = Usuario(
                id=row["id"],
                usuario=row["usuario"],
                id_rol=row["id_rol"],
                nombre_rol=row["nombre_rol"],
                nombre_completo=row.get("nombre_completo"),
                activo=bool(row.get("activo", 1)),
            )
            return True, user, "Bienvenido."
        except Exception as e:
            return False, None, f"Error: {e}"
        finally:
            cerrar_conexion(conn)
