# models/__init__.py
# OmniStock - Modelos de datos

from .productos import Producto
from .ventas import Venta, DetalleVenta
from .cliente import Cliente
from .usuario import Usuario, Rol

__all__ = ["Producto", "Venta", "DetalleVenta", "Cliente", "Usuario", "Rol"]
