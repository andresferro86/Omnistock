# OmniStock – Instrucciones para crear la base de datos y tablas

Estas instrucciones permiten crear la base de datos **omnistock**, las tablas y cargar los datos de prueba necesarios para la aplicación.

---

## Requisitos previos

- **MySQL** instalado y en ejecución (servidor local o remoto).
- Usuario con permisos para crear bases de datos (por ejemplo `root` o un usuario con privilegios).

---

## Opción 1: MySQL Workbench

1. Abre **MySQL Workbench** y conéctate al servidor (usuario y contraseña de MySQL).
2. Menú **File** → **Open SQL Script**.
3. Navega a la carpeta del proyecto y selecciona:
   ```
   OmniStock\database\schema.sql
   ```
   Ruta completa ejemplo: `c:\NetBeans\AppCursos\OmniStock\database\schema.sql`
4. Haz clic en el icono del **rayo** (Execute) o usa **Ctrl+Shift+Enter** para ejecutar todo el script.
5. Verifica en el panel izquierdo que existe la base de datos **omnistock** y las tablas:
   - `productos`
   - `ventas`
   - `detalle_ventas`

---

## Opción 2: Línea de comandos (mysql)

Abre **CMD** o **PowerShell** y ejecuta:

```bash
cd c:\NetBeans\AppCursos\OmniStock

mysql -u root -p < database\schema.sql
```

Te pedirá la contraseña de MySQL. Si tu usuario no es `root`, cambia `-u root` por tu usuario, por ejemplo:

```bash
mysql -u tu_usuario -p < database\schema.sql
```

**En PowerShell** puede ser necesario usar la ruta completa del ejecutable de MySQL, por ejemplo:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p < database\schema.sql
```

(Ajusta la ruta según tu instalación de MySQL.)

---

## Opción 3: Ejecutar el script desde dentro de MySQL

1. Conéctate al cliente MySQL:
   ```bash
   mysql -u root -p
   ```
2. Ejecuta el script indicando la ruta del archivo:
   ```sql
   source c:/NetBeans/AppCursos/OmniStock/database/schema.sql
   ```
   En Windows usa **barras normales** `/` en la ruta. Si prefieres barras invertidas, escápalas: `c:\\NetBeans\\AppCursos\\OmniStock\\database\\schema.sql`
3. Escribe `exit` para salir.

---

## Qué crea el script

| Paso | Descripción |
|------|-------------|
| 1 | Crea la base de datos **omnistock** (si no existe), con `utf8mb4`. |
| 2 | Crea la tabla **productos** (id, nombre, descripcion, precio, stock, fechas). |
| 3 | Crea la tabla **ventas** (id, fecha_venta, total, cliente, observaciones). |
| 4 | Crea la tabla **detalle_ventas** (id_venta, id_producto, cantidad, precio_unitario, subtotal) con claves foráneas. |
| 5 | Inserta **8 productos** de prueba (lápiz, cuaderno, borrador, etc.). |
| 6 | Inserta **1 venta de ejemplo** con 2 líneas y actualiza el stock de los productos. |

---

## Verificar que todo quedó bien

Conéctate a MySQL y ejecuta:

```sql
USE omnistock;

SELECT COUNT(*) AS total_productos FROM productos;
-- Debe mostrar 8 (o 6 si ya se descontó stock de la venta de ejemplo: 8 registros en total).

SELECT * FROM productos;
SELECT * FROM ventas;
SELECT * FROM detalle_ventas;
```

Deberías ver productos, al menos una venta y sus detalles.

---

## Configurar la aplicación (config.py)

Después de crear la base de datos, edita **config.py** en la raíz del proyecto y ajusta la conexión:

```python
# OmniStock\config.py

DB_CONFIG = {
    "host": "localhost",      # o la IP de tu servidor MySQL
    "user": "root",           # tu usuario de MySQL
    "password": "tu_contraseña",  # contraseña de MySQL
    "database": "omnistock",
    "charset": "utf8mb4",
    "autocommit": True,
}
```

Guarda el archivo y ejecuta la aplicación con `python main.py`.

---

## Volver a crear todo desde cero (reset)

Si quieres borrar la base de datos y volver a crearla con datos limpios:

```sql
DROP DATABASE IF EXISTS omnistock;
```

Luego ejecuta de nuevo el script **schema.sql** con cualquiera de las opciones anteriores.

**Nota:** No ejecutes el script **schema.sql** varias veces seguidas sin hacer `DROP DATABASE` si no quieres errores de filas duplicadas en los INSERT de productos. Para una instalación nueva, una sola ejecución es suficiente.

---

## Resumen rápido

| Acción | Comando o paso |
|--------|----------------|
| Crear BD y tablas con datos | Ejecutar `OmniStock\database\schema.sql` (Workbench o `mysql -u root -p < database\schema.sql`) |
| Configurar app | Editar `config.py` (user, password, host) |
| Ejecutar app | `python main.py` desde la carpeta `OmniStock` |
