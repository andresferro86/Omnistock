# services/clientes_service.py
# OmniStock - Servicio CRUD de clientes

"""
Lógica de negocio para clientes: listar, agregar, buscar, editar y eliminar.
"""

from typing import List, Optional, Tuple

from db.conexion import obtener_conexion, cerrar_conexion
from models.cliente import Cliente


class ClientesService:
    """Servicio para la gestión del catálogo de clientes."""

    @staticmethod
    def listar_todos() -> List[Cliente]:
        """Obtiene todos los clientes ordenados por nombre."""
        conn = obtener_conexion()
        if not conn:
            return []
        clientes = []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, nombre, documento, telefono, email, direccion, fecha_creacion "
                "FROM clientes ORDER BY nombre"
            )
            for row in cursor.fetchall():
                clientes.append(Cliente(
                    id=row["id"],
                    nombre=row["nombre"],
                    documento=row.get("documento"),
                    telefono=row.get("telefono"),
                    email=row.get("email"),
                    direccion=row.get("direccion"),
                    fecha_creacion=str(row["fecha_creacion"]) if row.get("fecha_creacion") else None,
                ))
            cursor.close()
        except Exception as e:
            print(f"Error listar clientes: {e}")
        finally:
            cerrar_conexion(conn)
        return clientes

    @staticmethod
    def buscar_por_id(id_cliente: int) -> Optional[Cliente]:
        """Obtiene un cliente por su ID."""
        conn = obtener_conexion()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, nombre, documento, telefono, email, direccion, fecha_creacion "
                "FROM clientes WHERE id = %s",
                (id_cliente,),
            )
            row = cursor.fetchone()
            cursor.close()
            if not row:
                return None
            return Cliente(
                id=row["id"],
                nombre=row["nombre"],
                documento=row.get("documento"),
                telefono=row.get("telefono"),
                email=row.get("email"),
                direccion=row.get("direccion"),
                fecha_creacion=str(row["fecha_creacion"]) if row.get("fecha_creacion") else None,
            )
        except Exception as e:
            print(f"Error buscar cliente: {e}")
            return None
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def buscar_por_texto(texto: str) -> List[Cliente]:
        """Busca clientes cuyo nombre, documento o email contenga el texto."""
        if not (texto or "").strip():
            return ClientesService.listar_todos()
        conn = obtener_conexion()
        if not conn:
            return []
        clientes = []
        try:
            cursor = conn.cursor(dictionary=True)
            patron = f"%{texto.strip()}%"
            cursor.execute(
                "SELECT id, nombre, documento, telefono, email, direccion, fecha_creacion "
                "FROM clientes WHERE nombre LIKE %s OR COALESCE(documento,'') LIKE %s OR COALESCE(email,'') LIKE %s ORDER BY nombre",
                (patron, patron, patron),
            )
            for row in cursor.fetchall():
                clientes.append(Cliente(
                    id=row["id"],
                    nombre=row["nombre"],
                    documento=row.get("documento"),
                    telefono=row.get("telefono"),
                    email=row.get("email"),
                    direccion=row.get("direccion"),
                    fecha_creacion=str(row["fecha_creacion"]) if row.get("fecha_creacion") else None,
                ))
            cursor.close()
        except Exception as e:
            print(f"Error buscar clientes: {e}")
        finally:
            cerrar_conexion(conn)
        return clientes

    @staticmethod
    def agregar(nombre: str, documento: str = "", telefono: str = "", email: str = "", direccion: str = "") -> Tuple[bool, str]:
        """Inserta un nuevo cliente."""
        nombre = (nombre or "").strip()
        if not nombre:
            return False, "El nombre del cliente no puede estar vacío."
        conn = obtener_conexion()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO clientes (nombre, documento, telefono, email, direccion) VALUES (%s, %s, %s, %s, %s)",
                (nombre, (documento or "").strip() or None, (telefono or "").strip() or None, (email or "").strip() or None, (direccion or "").strip() or None),
            )
            conn.commit()
            cursor.close()
            return True, "Cliente agregado correctamente."
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al agregar cliente: {e}"
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def editar(id_cliente: int, nombre: str, documento: str = "", telefono: str = "", email: str = "", direccion: str = "") -> Tuple[bool, str]:
        """Actualiza un cliente existente."""
        nombre = (nombre or "").strip()
        if not nombre:
            return False, "El nombre del cliente no puede estar vacío."
        conn = obtener_conexion()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE clientes SET nombre=%s, documento=%s, telefono=%s, email=%s, direccion=%s WHERE id=%s",
                (nombre, (documento or "").strip() or None, (telefono or "").strip() or None, (email or "").strip() or None, (direccion or "").strip() or None, id_cliente),
            )
            if cursor.rowcount == 0:
                cursor.close()
                return False, "No se encontró el cliente."
            conn.commit()
            cursor.close()
            return True, "Cliente actualizado correctamente."
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al actualizar cliente: {e}"
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def eliminar(id_cliente: int) -> Tuple[bool, str]:
        """Elimina un cliente por ID."""
        conn = obtener_conexion()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
            if cursor.rowcount == 0:
                cursor.close()
                return False, "No se encontró el cliente."
            conn.commit()
            cursor.close()
            return True, "Cliente eliminado correctamente."
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al eliminar cliente: {e}"
        finally:
            cerrar_conexion(conn)
