# models/productos.py
# OmniStock - Modelo de entidad Producto

"""
Representa un producto en el sistema.
Atributos alineados con la tabla 'productos' de la base de datos.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class Producto:
    """Modelo de un producto con id, nombre, descripción, precio y stock."""

    id: int
    nombre: str
    descripcion: Optional[str]
    precio: Decimal
    stock: int
    fecha_creacion: Optional[str] = None
    fecha_actualizacion: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.precio, (int, float)):
            self.precio = Decimal(str(self.precio))

    def tiene_stock_suficiente(self, cantidad: int) -> bool:
        """Indica si hay stock suficiente para la cantidad solicitada."""
        return self.stock >= cantidad and cantidad > 0
