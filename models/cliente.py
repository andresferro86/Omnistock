# models/cliente.py
# OmniStock - Modelo de entidad Cliente

"""
Representa un cliente en el sistema.
Alineado con la tabla 'clientes' de la base de datos.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Cliente:
    """Modelo de un cliente con id, nombre, documento, teléfono, email, dirección."""

    id: int
    nombre: str
    documento: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    fecha_creacion: Optional[str] = None
