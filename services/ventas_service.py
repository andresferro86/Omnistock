# services/ventas_service.py
# OmniStock - Servicio de ventas (registro y historial)

"""
Lógica de negocio para ventas: registrar venta, descontar stock y consultar historial.
Valida stock suficiente antes de vender.
"""

from decimal import Decimal
from typing import List, Optional, Tuple

from db.conexion import obtener_conexion, cerrar_conexion
from models.ventas import Venta, DetalleVenta
from models.productos import Producto
from services.inventario_service import InventarioService


# Tipo: lista de (id_producto, cantidad, precio_unitario)
LineaVenta = Tuple[int, int, Decimal]


class VentasService:
    """Servicio para registrar ventas y consultar historial."""

    @staticmethod
    def validar_lineas(lineas: List[LineaVenta]) -> Tuple[bool, str]:
        """
        Valida que cada línea tenga cantidad > 0, precio >= 0 y stock suficiente.
        lineas: [(id_producto, cantidad, precio_unitario), ...]
        Returns:
            (es_valido, mensaje_error)
        """
        if not lineas:
            return False, "Debe agregar al menos un producto a la venta."
        for id_producto, cantidad, precio in lineas:
            if cantidad <= 0:
                return False, "La cantidad debe ser mayor que cero."
            if precio < 0:
                return False, "El precio no puede ser negativo."
            producto = InventarioService.buscar_por_id(id_producto)
            if not producto:
                return False, f"No existe el producto con ID {id_producto}."
            if not producto.tiene_stock_suficiente(cantidad):
                return False, f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}."
        return True, ""

    @staticmethod
    def registrar_venta(lineas: List[LineaVenta], cliente: str = "", observaciones: str = "") -> Tuple[bool, str]:
        """
        Registra una venta: inserta cabecera, detalles y descuenta stock.
        lineas: [(id_producto, cantidad, precio_unitario), ...]
        Returns:
            (exito, mensaje)
        """
        ok, msg = VentasService.validar_lineas(lineas)
        if not ok:
            return False, msg

        total = sum(cant * float(precio) for _, cant, precio in lineas)
        conn = obtener_conexion()
        if not conn:
            return False, "No se pudo conectar a la base de datos."
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO ventas (total, cliente, observaciones) VALUES (%s, %s, %s)",
                (float(total), (cliente or "").strip() or None, (observaciones or "").strip() or None),
            )
            id_venta = cursor.lastrowid
            for id_producto, cantidad, precio_unitario in lineas:
                subtotal = cantidad * float(precio_unitario)
                cursor.execute(
                    "INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, subtotal) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (id_venta, id_producto, cantidad, float(precio_unitario), subtotal),
                )
                cursor.execute("UPDATE productos SET stock = stock - %s WHERE id = %s", (cantidad, id_producto))
            conn.commit()
            cursor.close()
            return True, f"Venta registrada correctamente. Total: {total:.2f}"
        except Exception as e:
            if conn:
                conn.rollback()
            return False, f"Error al registrar la venta: {e}"
        finally:
            cerrar_conexion(conn)

    @staticmethod
    def listar_ventas() -> List[Venta]:
        """Obtiene todas las ventas ordenadas por fecha descendente."""
        conn = obtener_conexion()
        if not conn:
            return []
        ventas = []
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, fecha_venta, total, cliente, observaciones FROM ventas ORDER BY fecha_venta DESC"
            )
            for row in cursor.fetchall():
                v = Venta(
                    id=row["id"],
                    fecha_venta=str(row["fecha_venta"]),
                    total=row["total"],
                    cliente=row["cliente"],
                    observaciones=row["observaciones"],
                )
                cursor2 = conn.cursor(dictionary=True)
                cursor2.execute(
                    "SELECT dv.id, dv.id_venta, dv.id_producto, p.nombre AS nombre_producto, "
                    "dv.cantidad, dv.precio_unitario, dv.subtotal "
                    "FROM detalle_ventas dv JOIN productos p ON dv.id_producto = p.id WHERE dv.id_venta = %s",
                    (v.id,),
                )
                for d in cursor2.fetchall():
                    v.detalles.append(DetalleVenta(
                        id=d["id"],
                        id_venta=d["id_venta"],
                        id_producto=d["id_producto"],
                        nombre_producto=d["nombre_producto"],
                        cantidad=d["cantidad"],
                        precio_unitario=d["precio_unitario"],
                        subtotal=d["subtotal"],
                    ))
                cursor2.close()
                ventas.append(v)
            cursor.close()
        except Exception as e:
            print(f"Error listar ventas: {e}")
        finally:
            cerrar_conexion(conn)
        return ventas
