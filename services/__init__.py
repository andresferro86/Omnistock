# services/__init__.py
# OmniStock - Servicios de negocio

from .inventario_service import InventarioService
from .ventas_service import VentasService

__all__ = ["InventarioService", "VentasService"]
