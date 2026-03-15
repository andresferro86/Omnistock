# services/inventario_service.py
# OmniStock - Servicio de inventario (CRUD productos)

"""
Lógica de negocio para productos: listar, agregar, buscar, editar y eliminar.
Incluye validaciones (nombre no vacío, precios y stock no negativos).
"""

from decimal import Decimal
from typing import List, Optional, Tuple

from db.conexion import obtener_conexion, cerrar_conexion
from models.productos import Producto
from utils.helpers import validar_decimal_positivo, validar_entero_positivo


class InventarioService:
    """Servicio para la gestión de productos en el inventario."""

    @staticmethod
    def listar_todos() -> List[Producto]:
        """Obtiene todos los productos ordenados por nombre."""
        conn = obtener_conexion()
        if not conn:
            return []
        productos = []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, nombre, descripcion, precio, stock, fecha_creacion, fecha_actualizacion "
                "FROM productos ORDER BY nombre"
            )
            for row in cursor.fetchall():
                productos.append(Producto(
                    id=row["id"],
                    nombre=row["nombre"],
                    descripcion=row["descripcion"],
                    precio=row["precio"],
                    stock=row["stock"],
                    fecha_creacion=str(row["fecha_creacion"]) if row.get("fecha_creacion") else None,
                    fecha_actualizacion=str(row["fecha_actualizacion"]) if row.get("fecha_actualizacion") else None,
                ))
            cursor.close()
        except Exception as e:
            print(f"Error listar productos: {e}")
        finally:
            cerrar_conexion(conn)
        return productos

    @staticmethod
    def buscar_por_id(id_producto: int) -> Optional[Producto]:
        """Obtiene un producto por su ID."""
        conn = obtener_conexion()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, nombre, descripcion, precio, stock, fecha_creacion, fecha_actualizacion "
                "FROM productos WHERE id = %s",
                (id_producto,),
            )
            row = cursor.fetchone()
            cursor.close()
            if not row:
                return None
            return Producto(
                id=row["id"],
                nombre=row["nombre"],
                descripcion=row["descripcion"],
                precio=row["precio"],
                stock=row["stock"],
                fecha_creacion=str(row["fecha_creacion"]) if row.get("fecha_creacion") else None,
                fecha_actualizacion=str(row["fecha_actualizacion"]) if row.get("fecha_actualizacion") else None,
            )
        except Exception as e:
            print(f"Error buscar producto: {e}")
            return None
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def buscar_por_texto(texto: str) -> List[Producto]:
        """Busca productos cuyo nombre o descripción contenga el texto."""
        if not (texto or "").strip():
            return InventarioService.listar_todos()
        conn = obtener_conexion()
        if not conn:
            return []
        productos = []
        try:
            cursor = conn.cursor(dictionary=True)
            patron = f"%{texto.strip()}%"
            cursor.execute(
                "SELECT id, nombre, descripcion, precio, stock, fecha_creacion, fecha_actualizacion "
                "FROM productos WHERE nombre LIKE %s OR COALESCE(descripcion,'') LIKE %s ORDER BY nombre",
                (patron, patron),
            )
            for row in cursor.fetchall():
                productos.append(Producto(
                    id=row["id"],
                    nombre=row["nombre"],
                    descripcion=row["descripcion"],
                    precio=row["precio"],
                    stock=row["stock"],
                    fecha_creacion=str(row["fecha_creacion"]) if row.get("fecha_creacion") else None,
                    fecha_actualizacion=str(row["fecha_actualizacion"]) if row.get("fecha_actualizacion") else None,
                ))
            cursor.close()
        except Exception as e:
            print(f"Error buscar productos: {e}")
        finally:
            cerrar_conexion(conn)
        return productos

    @staticmethod
    def validar_producto(nombre: str, precio_str: str, stock_str: str, descripcion: str = "") -> Tuple[bool, str]:
        """
        Valida nombre no vacío, precio y stock numéricos y no negativos.
        Returns:
            (es_valido, mensaje_error)
        """
        nombre = (nombre or "").strip()
        if not nombre:
            return False, "El nombre del producto no puede estar vacío."
        ok_precio, precio, msg_precio = validar_decimal_positivo(precio_str, "El precio")
        if not ok_precio:
            return False, msg_precio
        ok_stock, stock, msg_stock = validar_entero_positivo(stock_str, "El stock")
        if not ok_stock:
            return False, msg_stock
        return True, ""

    @staticmethod
    def agregar(nombre: str, precio: Decimal, stock: int, descripcion: str = "") -> Tuple[bool, str]:
        """
        Inserta un nuevo producto.
        Returns:
            (exito, mensaje)
        """
        nombre = (nombre or "").strip()
        if not nombre:
            return False, "El nombre del producto no puede estar vacío."
        if precio < 0:
            return False, "El precio no puede ser negativo."
        if stock < 0:
            return False, "El stock no puede ser negativo."
        conn = obtener_conexion()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
                (nombre, (descripcion or "").strip() or None, float(precio), stock),
            )
            conn.commit()
            cursor.close()
            return True, "Producto agregado correctamente."
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al agregar producto: {e}"
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def editar(id_producto: int, nombre: str, precio: Decimal, stock: int, descripcion: str = "") -> Tuple[bool, str]:
        """
        Actualiza un producto existente.
        Returns:
            (exito, mensaje)
        """
        nombre = (nombre or "").strip()
        if not nombre:
            return False, "El nombre del producto no puede estar vacío."
        if precio < 0:
            return False, "El precio no puede ser negativo."
        if stock < 0:
            return False, "El stock no puede ser negativo."
        conn = obtener_conexion()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s WHERE id=%s",
                (nombre, (descripcion or "").strip() or None, float(precio), stock, id_producto),
            )
            if cursor.rowcount == 0:
                cursor.close()
                return False, "No se encontró el producto."
            conn.commit()
            cursor.close()
            return True, "Producto actualizado correctamente."
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al actualizar producto: {e}"
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def eliminar(id_producto: int) -> Tuple[bool, str]:
        """
        Elimina un producto por ID.
        Returns:
            (exito, mensaje)
        """
        conn = obtener_conexion()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
            if cursor.rowcount == 0:
                cursor.close()
                return False, "No se encontró el producto."
            conn.commit()
            cursor.close()
            return True, "Producto eliminado correctamente."
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al eliminar producto: {e}"
        finally:
            cerrar_conexion(conn)
