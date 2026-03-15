# db/conexion.py
# OmniStock - Gestión de la conexión a MySQL

"""
Módulo que centraliza la conexión a la base de datos MySQL.
Proporciona una función para obtener conexión y otra para cerrarla.
"""

import mysql.connector
from mysql.connector import Error

# Importar configuración desde el directorio raíz del proyecto
import sys
from pathlib import Path

# Asegurar que el directorio raíz esté en el path
raiz = Path(__file__).resolve().parent.parent
if str(raiz) not in sys.path:
    sys.path.insert(0, str(raiz))

from config import DB_CONFIG


def obtener_conexion():
    """
    Crea y devuelve una conexión a la base de datos MySQL.
    Returns:
        Conexión de mysql.connector o None si hay error.
    """
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None


def cerrar_conexion(conexion):
    """
    Cierra la conexión de forma segura.
    Args:
        conexion: Objeto conexión de mysql.connector.
    """
    if conexion and conexion.is_connected():
        conexion.close()
