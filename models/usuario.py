# models/usuario.py
# OmniStock - Modelos Usuario y Rol (autenticación y autorización)

"""
Modelos para usuario y rol. Alineados con las tablas 'usuarios' y 'roles'.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Rol:
    """Rol del usuario (Administrador, Vendedor, etc.)."""

    id: int
    nombre: str


@dataclass
class Usuario:
    """Usuario del sistema (login, rol, nombre)."""

    id: int
    usuario: str
    id_rol: int
    nombre_rol: str  # Para mostrar en UI
    nombre_completo: Optional[str] = None
    activo: bool = True
