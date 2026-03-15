# config.py
# OmniStock - Configuración de la aplicación y conexión a MySQL

"""
Configuración centralizada para OmniStock.
Modifica aquí los datos de conexión a MySQL según tu entorno.
"""

# Parámetros de conexión a MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Coloca tu contraseña de MySQL
    "database": "omnistock",
    "charset": "utf8mb4",
    "autocommit": True,
}

# Opcional: puerto (por defecto MySQL usa 3306)
# "port": 3306,
