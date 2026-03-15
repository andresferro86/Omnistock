# OmniStock - Sistema de Gestión de Inventario y Ventas

Proyecto académico (ACA): aplicación de escritorio en **Python** con **Tkinter** y base de datos **MySQL**.

## Requisitos

- **Python 3.8+** (Tkinter suele venir incluido)
- **MySQL** (servidor local o remoto)
- **mysql-connector-python**

## Instalación

1. **Clonar o copiar** el proyecto en una carpeta (por ejemplo `OmniStock`).

2. **Crear el entorno virtual** (recomendado):
   - En **Windows** (PowerShell o CMD), si `python` no funciona, usa el launcher `py`:
   ```powershell
   cd OmniStock
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   - En CMD: `venv\Scripts\activate.bat`
   - En Linux/Mac: `python3 -m venv venv` y `source venv/bin/activate`

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar MySQL**:
   - Crear la base de datos y tablas ejecutando el script:
     ```bash
     mysql -u root -p < database/schema.sql
     ```
     O abrir `database/schema.sql` en MySQL Workbench y ejecutarlo.
   - Editar `config.py` y ajustar `host`, `user`, `password` y `database` según tu instalación de MySQL.

## Ejecución

Desde la carpeta del proyecto (con el entorno virtual activado si lo usas):

```bash
python main.py
```
En Windows, si `python` no está en PATH, usa: `py main.py`

Al iniciar se muestra la **pantalla de login**. Usuario y contraseña por defecto (creados al primer arranque si no hay usuarios): **admin** / **admin**. Tras iniciar sesión se abre la ventana principal con tres pestañas: **Productos**, **Clientes** y **Ventas**.

## Estructura del proyecto

- `main.py` — Punto de entrada (muestra login y luego ventana principal).
- `config.py` — Configuración de conexión MySQL.
- `db/conexion.py` — Conexión a la base de datos.
- `models/` — Modelos Producto, Venta, DetalleVenta, Cliente, Usuario, Rol.
- `services/` — Lógica de negocio (inventario, ventas, clientes, autenticación).
- `ui/` — Ventanas Tkinter (login, principal, productos, clientes, ventas).
- `utils/helpers.py` — Validaciones y formato.
- `database/schema.sql` — Script SQL completo (productos, ventas, clientes, usuarios, roles).

## Funcionalidades

- **Login:** autenticación con usuario y contraseña (hash bcrypt). Roles: Administrador, Vendedor. Usuario por defecto: admin / admin.
- **Productos:** listar, buscar, agregar, editar, eliminar (CRUD).
- **Clientes:** listar, buscar, agregar, editar, eliminar (CRUD). En Ventas se puede elegir un cliente del catálogo o escribir nombre libre.
- **Ventas:** agregar productos a una venta, registrar venta (descuenta stock), ver historial.
- Validaciones: nombre no vacío donde aplica, precios y cantidades no negativos, stock suficiente al vender.

## Posibles mejoras futuras

- Exportar reportes (PDF/Excel).
- Gráficos de ventas.
- Módulo de usuarios y permisos.
- Búsqueda avanzada y filtros por fecha en historial de ventas.
