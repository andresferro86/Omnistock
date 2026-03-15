# models/__init__.py
# OmniStock - Modelos de datos

from .productos import Producto
from .ventas import Venta, DetalleVenta

__all__ = ["Producto", "Venta", "DetalleVenta"]
