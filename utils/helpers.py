# utils/helpers.py
# OmniStock - Funciones auxiliares y validaciones

"""
Funciones de validación y formato reutilizables en toda la aplicación.
"""

from decimal import Decimal, InvalidOperation
from typing import Optional, Tuple


def validar_entero_positivo(valor: str, nombre_campo: str = "Cantidad") -> Tuple[bool, Optional[int], str]:
    """
    Valida que una cadena sea un entero >= 0.
    Returns:
        (es_valido, valor_entero, mensaje_error)
    """
    valor = (valor or "").strip()
    if not valor:
        return False, None, f"{nombre_campo} no puede estar vacío."
    try:
        n = int(valor)
        if n < 0:
            return False, None, f"{nombre_campo} no puede ser negativo."
        return True, n, ""
    except ValueError:
        return False, None, f"{nombre_campo} debe ser un número entero."


def validar_decimal_positivo(valor: str, nombre_campo: str = "Precio") -> Tuple[bool, Optional[Decimal], str]:
    """
    Valida que una cadena sea un número decimal >= 0.
    Returns:
        (es_valido, valor_decimal, mensaje_error)
    """
    valor = (valor or "").strip().replace(",", ".")
    if not valor:
        return False, None, f"{nombre_campo} no puede estar vacío."
    try:
        d = Decimal(valor)
        if d < 0:
            return False, None, f"{nombre_campo} no puede ser negativo."
        return True, d, ""
    except (InvalidOperation, ValueError):
        return False, None, f"{nombre_campo} debe ser un número válido."


def formatear_precio(valor) -> str:
    """Formatea un número como precio con dos decimales."""
    try:
        if isinstance(valor, (int, float)):
            return f"{float(valor):.2f}"
        d = Decimal(str(valor))
        return f"{d:.2f}"
    except (TypeError, InvalidOperation, ValueError):
        return "0.00"
