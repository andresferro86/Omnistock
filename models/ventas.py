# models/ventas.py
# OmniStock - Modelos de Venta y Detalle de Venta

"""
Modelos para la cabecera de venta y las líneas (detalle).
Alineados con las tablas 'ventas' y 'detalle_ventas'.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional


@dataclass
class DetalleVenta:
    """Una línea de una venta: producto, cantidad, precio unitario y subtotal."""

    id: Optional[int]
    id_venta: Optional[int]
    id_producto: int
    nombre_producto: str  # Para mostrar en listados
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal

    def __post_init__(self):
        if isinstance(self.precio_unitario, (int, float)):
            self.precio_unitario = Decimal(str(self.precio_unitario))
        if isinstance(self.subtotal, (int, float)):
            self.subtotal = Decimal(str(self.subtotal))


@dataclass
class Venta:
    """Cabecera de una venta: id, fecha, total, cliente y lista de detalles."""

    id: int
    fecha_venta: str
    total: Decimal
    cliente: Optional[str] = None
    observaciones: Optional[str] = None
    detalles: List[DetalleVenta] = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.total, (int, float)):
            self.total = Decimal(str(self.total))
