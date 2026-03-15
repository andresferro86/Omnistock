# db/__init__.py
# OmniStock - Módulo de base de datos

from .conexion import obtener_conexion, cerrar_conexion

__all__ = ["obtener_conexion", "cerrar_conexion"]
