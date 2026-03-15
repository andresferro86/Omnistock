# services/usuarios_service.py
# OmniStock - CRUD de usuarios (solo Admin)

"""
Listar, agregar, editar y eliminar usuarios. Contraseñas con hash bcrypt.
"""

from typing import List, Optional, Tuple

from db.conexion import obtener_conexion, cerrar_conexion
from models.usuario import Usuario
from services.auth_service import AuthService


class UsuariosService:
    """Servicio para administrar usuarios (solo rol Administrador)."""

    @staticmethod
    def listar_todos() -> List[Usuario]:
        """Lista todos los usuarios con su rol."""
        conn = obtener_conexion()
        if not conn:
            return []
        usuarios = []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT u.id, u.usuario, u.id_rol, u.nombre_completo, u.activo, r.nombre AS nombre_rol "
                "FROM usuarios u JOIN roles r ON u.id_rol = r.id ORDER BY u.usuario"
            )
            for row in cursor.fetchall():
                usuarios.append(Usuario(
                    id=row["id"],
                    usuario=row["usuario"],
                    id_rol=row["id_rol"],
                    nombre_rol=row["nombre_rol"],
                    nombre_completo=row.get("nombre_completo"),
                    activo=bool(row.get("activo", 1)),
                ))
            cursor.close()
        except Exception as e:
            print(f"Error listar usuarios: {e}")
        finally:
            cerrar_conexion(conn)
        return usuarios

    @staticmethod
    def buscar_por_id(id_usuario: int) -> Optional[Usuario]:
        conn = obtener_conexion()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT u.id, u.usuario, u.id_rol, u.nombre_completo, u.activo, r.nombre AS nombre_rol "
                "FROM usuarios u JOIN roles r ON u.id_rol = r.id WHERE u.id = %s",
                (id_usuario,),
            )
            row = cursor.fetchone()
            cursor.close()
            if not row:
                return None
            return Usuario(
                id=row["id"],
                usuario=row["usuario"],
                id_rol=row["id_rol"],
                nombre_rol=row["nombre_rol"],
                nombre_completo=row.get("nombre_completo"),
                activo=bool(row.get("activo", 1)),
            )
        except Exception as e:
            print(f"Error buscar usuario: {e}")
            return None
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def listar_roles() -> List[Tuple[int, str]]:
        """Devuelve [(id_rol, nombre_rol), ...]."""
        conn = obtener_conexion()
        if not conn:
            return []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM roles ORDER BY id")
            out = [(row[0], row[1]) for row in cursor.fetchall()]
            cursor.close()
            return out
        except Exception as e:
            print(f"Error listar roles: {e}")
            return []
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def agregar(usuario: str, password: str, id_rol: int, nombre_completo: str = "") -> Tuple[bool, str]:
        usuario = (usuario or "").strip()
        if not usuario:
            return False, "El usuario no puede estar vacío."
        if not (password or "").strip():
            return False, "La contraseña no puede estar vacía."
        conn = obtener_conexion()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor()
            password_hash = AuthService._hash_password((password or "").strip()[:72])
            cursor.execute(
                "INSERT INTO usuarios (usuario, password_hash, id_rol, nombre_completo, activo) VALUES (%s, %s, %s, %s, 1)",
                (usuario, password_hash, id_rol, (nombre_completo or "").strip() or None),
            )
            conn.commit()
            cursor.close()
            return True, "Usuario agregado correctamente."
        except Exception as e:
            if conn:
                conn.rollback()
            err = str(e).lower()
            if "duplicate" in err or "unique" in err:
                return False, "Ya existe un usuario con ese nombre."
            return False, f"Error al agregar usuario: {e}"
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def editar(id_usuario: int, id_rol: int, nombre_completo: str = "", activo: bool = True, nueva_password: Optional[str] = None) -> Tuple[bool, str]:
        conn = obtener_conexion()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor()
            if (nueva_password or "").strip():
                password_hash = AuthService._hash_password(nueva_password.strip()[:72])
                cursor.execute(
                    "UPDATE usuarios SET id_rol=%s, nombre_completo=%s, activo=%s, password_hash=%s WHERE id=%s",
                    (id_rol, (nombre_completo or "").strip() or None, 1 if activo else 0, password_hash, id_usuario),
                )
            else:
                cursor.execute(
                    "UPDATE usuarios SET id_rol=%s, nombre_completo=%s, activo=%s WHERE id=%s",
                    (id_rol, (nombre_completo or "").strip() or None, 1 if activo else 0, id_usuario),
                )
            if cursor.rowcount == 0:
                cursor.close()
                return False, "No se encontró el usuario."
            conn.commit()
            cursor.close()
            return True, "Usuario actualizado correctamente."
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al actualizar usuario: {e}"
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def eliminar(id_usuario: int) -> Tuple[bool, str]:
        """Elimina el usuario. No permite eliminar si es el último Administrador."""
        usuarios = UsuariosService.listar_todos()
        admins = [u for u in usuarios if u.nombre_rol == "Administrador"]
        target = next((u for u in usuarios if u.id == id_usuario), None)
        if not target:
            return False, "No se encontró el usuario."
        if target.nombre_rol == "Administrador" and len(admins) <= 1:
            return False, "No se puede eliminar el último Administrador."
        conn = obtener_conexion()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
            if cursor.rowcount == 0:
                cursor.close()
                return False, "No se encontró el usuario."
            conn.commit()
            cursor.close()
            return True, "Usuario eliminado correctamente."
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al eliminar usuario: {e}"
        finally:
            cerrar_conexion(conn)
