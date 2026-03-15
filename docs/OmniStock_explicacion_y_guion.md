# OmniStock — Explicación técnica y guion de exposición en video

**Proyecto final — Programación Avanzada**  
Documento de apoyo para la sustentación del aplicativo, el código y la base de datos.

---

## Índice

1. [Explicación técnica del programa](#1-explicación-técnica-del-programa)
2. [Inicio del sistema, login y roles](#2-inicio-del-sistema-login-y-roles)
3. [Conexión a la base de datos MySQL](#3-conexión-a-la-base-de-datos-mysql)
4. [Estructura del proyecto](#4-estructura-del-proyecto)
5. [Modelo de base de datos](#5-modelo-de-base-de-datos)
6. [Módulo de productos (CRUD)](#6-funcionamiento-del-módulo-de-productos)
7. [Módulo de clientes (CRUD)](#7-módulo-de-clientes-crud)
8. [Módulo de usuarios (CRUD, solo Administrador)](#8-módulo-de-usuarios-crud-solo-administrador)
9. [Módulo de ventas y transacciones](#9-módulo-de-ventas-y-transacciones)
10. [Comunicación interfaz ↔ base de datos](#10-comunicación-entre-la-interfaz-y-la-base-de-datos)
11. [Actualización de la interfaz (refresco de datos)](#11-actualización-de-la-interfaz)
12. [Seguridad y buenas prácticas](#12-seguridad-y-buenas-prácticas)
13. [Conclusión técnica](#13-conclusión-técnica)
14. [Guion de exposición (3 personas)](#14-guion-de-exposición-dividido-en-3-personas)
15. [Recomendaciones para la grabación](#15-recomendaciones-para-la-grabación)
16. [Frases útiles](#16-frases-útiles)

---

## 1. Explicación técnica del programa

**OmniStock** es un Sistema de Gestión de Inventario y Ventas desarrollado en **Python**, con interfaz gráfica en **Tkinter** (ttk) y base de datos relacional en **MySQL**. Su objetivo es digitalizar procesos básicos del negocio: administrar productos, clientes y usuarios; registrar ventas; y actualizar el inventario en tiempo real.

Desde el punto de vista técnico, el sistema integra **tres capas**:

- **Capa de presentación (UI):** formularios, tablas, botones y ventanas (Tkinter/ttk); login y ventana principal según rol.
- **Capa de lógica de negocio (services):** validaciones, reglas de stock, proceso de ventas, autenticación (bcrypt), CRUD de productos, clientes y usuarios.
- **Capa de datos:** conexión a MySQL, ejecución de consultas parametrizadas y modelos (Producto, Venta, DetalleVenta, Cliente, Usuario, Rol).

Esta separación mejora el mantenimiento, facilita la depuración y asigna una responsabilidad clara a cada módulo.

---

## 2. Inicio del sistema, login y roles

El programa inicia en **main.py**. El flujo es:

1. **main.py** importa `LoginView` y `MainWindow`, define un callback `on_login_ok(usuario)` que crea y ejecuta `MainWindow(usuario=usuario)`.
2. Se muestra la ventana de **login** (`ui/login_view.py`). El usuario ingresa usuario y contraseña.
3. **AuthService** (`services/auth_service.py`) valida contra la tabla `usuarios`: las contraseñas se almacenan con hash **bcrypt** (no en texto plano). Si no existe ningún usuario en la BD, el sistema crea uno por defecto (admin / admin).
4. Al validar correctamente, la ventana de login se **cierra** (`destroy`) y se abre la **ventana principal** con el usuario logueado.
5. Según el **rol** del usuario (Administrador o Vendedor), la ventana principal muestra unas u otras pestañas:

| Rol              | Productos        | Clientes | Ventas | Usuarios   |
|------------------|------------------|----------|--------|------------|
| **Administrador**| CRUD completo    | CRUD     | Sí     | CRUD       |
| **Vendedor**     | Solo **Stock** (consulta, sin formulario ni botones CRUD) | CRUD | Sí | No visible |

El **Vendedor** puede ver la cantidad en stock, registrar ventas y crear/editar clientes; no puede administrar productos ni usuarios.

---

## 3. Conexión a la base de datos MySQL

### Entorno: Wampserver y MySQL

El servidor MySQL se ejecuta mediante **Wampserver** (en este proyecto se usó Wampserver 3.4.0 - 64bit). El motor de base de datos por defecto es **MySQL 8.4.7** (no MariaDB). Es importante que antes de ejecutar OmniStock el servicio MySQL esté en marcha: en la bandeja del sistema, icono de Wampserver (W), comprobar que MySQL figure con el indicador verde (en ejecución). Si no, usar **Start All Services** o iniciar solo el servicio MySQL. La configuración avanzada del servidor (puerto, memoria, etc.) está en el archivo **my.ini**, accesible desde el menú de Wampserver: clic derecho en el icono → MySQL → **my.ini**.

La aplicación se conecta a ese MySQL en **localhost** (puerto 3306 por defecto). Las credenciales y el nombre de la base de datos se definen en **config.py** en el proyecto; el usuario típico en una instalación local de Wampserver es `root` con contraseña vacía o la que se haya configurado en MySQL.

### Configuración en el proyecto (config.py y db/conexion.py)

La configuración de conexión que usa la aplicación se centraliza en **config.py**, con parámetros como host, usuario, contraseña, base de datos y codificación. La base de datos se llama **omnistock** y, por defecto, se conecta a **localhost**.

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Configurar según el entorno (Wampserver: a menudo vacía para root)
    "database": "omnistock",
    "charset": "utf8mb4",
    "autocommit": True,
}
```

El módulo **db/conexion.py** encapsula la conexión usando **mysql-connector-python**:

- `obtener_conexion()`: crea y devuelve una conexión a MySQL (al servidor gestionado por Wampserver).
- `cerrar_conexion(conexion)`: cierra la conexión de forma segura.

Los servicios (inventario, ventas, clientes, usuarios, auth) usan estas funciones para abrir conexión, ejecutar consultas con cursor y cerrar al terminar, sin repetir código en cada módulo.

---

## 4. Estructura del proyecto

El proyecto está organizado por capas y por responsabilidad:

| Elemento | Función |
|----------|---------|
| **main.py** | Punto de entrada; muestra login y, al validar, abre MainWindow con el usuario. |
| **config.py** | Configuración central (DB_CONFIG). |
| **db/conexion.py** | Obtención y cierre de conexión MySQL. |
| **models/** | Entidades: Producto, Venta, DetalleVenta, Cliente, Usuario (dataclasses). |
| **services/** | Lógica de negocio: InventarioService, VentasService, ClientesService, AuthService, UsuariosService. |
| **ui/** | Login (login_view), ventana principal (main_window) y vistas: Productos, Clientes, Ventas, Usuarios. |
| **utils/helpers.py** | Validaciones y formato (precios, enteros, decimales). |
| **database/schema.sql** | Script para crear la BD, tablas (productos, roles, usuarios, clientes, ventas, detalle_ventas) y datos de prueba. |
| **docs/** | Documentación (arquitectura, BD, guion). |

La interfaz muestra la información según el rol; los servicios aplican reglas y validaciones; la base de datos persiste los datos.

---

## 5. Modelo de base de datos

- **roles:** id, nombre (Administrador, Vendedor).
- **usuarios:** id, usuario (login), password_hash (bcrypt), id_rol (FK → roles), nombre_completo, activo, fecha_creacion.
- **productos:** id, nombre, descripcion, precio (DECIMAL), stock (INT), fecha_creacion, fecha_actualizacion. Índices en nombre y stock.
- **clientes:** id, nombre, documento, telefono, email, direccion, fecha_creacion. Índice en nombre.
- **ventas:** id, fecha_venta (DATETIME, default NOW()), total, id_cliente (FK → clientes, opcional), cliente (texto libre), observaciones. Índices en fecha_venta e id_cliente.
- **detalle_ventas:** id, id_venta (FK → ventas), id_producto (FK → productos), cantidad, precio_unitario, subtotal. ON DELETE CASCADE en id_venta.

Todos los importes están en **pesos**. El script completo está en **database/schema.sql**.

---

## 6. Funcionamiento del módulo de productos

El módulo de productos implementa un **CRUD completo** para el rol **Administrador**: crear, consultar, actualizar y eliminar. Para el rol **Vendedor**, la pestaña se llama **Stock** y es de solo lectura (listado y búsqueda para ver cantidades). Cada operación permitida se refleja en MySQL y la interfaz se actualiza.

**Consultas representativas:** (ver tabla de ubicación más abajo.)

### Ubicación de las consultas CRUD en el código (productos)

Todas las consultas del módulo de productos están en **un solo archivo**: `services/inventario_service.py`. La interfaz (`ui/productos_view.py`) no ejecuta SQL; llama a los métodos del servicio. Para el Vendedor se usa el mismo servicio pero con la vista en modo solo lectura (`solo_lectura=True`).

| Operación | Método | Archivo | Líneas aprox. |
|-----------|--------|---------|----------------|
| **SELECT – listar todos** (cargar tabla) | `listar_todos()` | `services/inventario_service.py` | 29-31 |
| **SELECT – buscar por ID** (un producto) | `buscar_por_id()` | `services/inventario_service.py` | 57-61 |
| **SELECT – búsqueda por texto** (campo Buscar, LIKE) | `buscar_por_texto()` | `services/inventario_service.py` | 94-97 |
| **INSERT – crear producto** (botón Guardar) | `agregar()` | `services/inventario_service.py` | 152-155 |
| **UPDATE – editar producto** (botón Actualizar) | `editar()` | `services/inventario_service.py` | 185-187 |
| **DELETE – eliminar producto** (botón Eliminar) | `eliminar()` | `services/inventario_service.py` | 214 |

**Desde la interfaz (`ui/productos_view.py`):** cargar o refrescar → `InventarioService.listar_todos()` o `buscar_por_texto()`; Guardar (nuevo) → `agregar()`; Actualizar → `editar()`; Eliminar → `eliminar()`. (En modo Vendedor solo se usan listar y buscar.)

---

## 7. Módulo de clientes (CRUD)

El módulo de clientes permite **listar, agregar, editar y eliminar** clientes. Lo usan tanto **Administrador** como **Vendedor** (por ejemplo para asociar un cliente a una venta o crear uno nuevo).

**Ubicación:** `services/clientes_service.py`. Vista: `ui/clientes_view.py`.

| Operación | Método | Archivo | Líneas aprox. |
|-----------|--------|---------|----------------|
| **SELECT – listar todos** | `listar_todos()` | `services/clientes_service.py` | 25-28 |
| **SELECT – buscar por ID** | `buscar_por_id()` | `services/clientes_service.py` | 54-57 |
| **SELECT – búsqueda por texto** | `buscar_por_texto()` | `services/clientes_service.py` | 91-94 |
| **INSERT – crear cliente** | `agregar()` | `services/clientes_service.py` | 124-126 |
| **UPDATE – editar cliente** | `editar()` | `services/clientes_service.py` | 150-152 |
| **DELETE – eliminar cliente** | `eliminar()` | `services/clientes_service.py` | 174 |

Validación: el nombre del cliente no puede estar vacío.

---

## 8. Módulo de usuarios (CRUD, solo Administrador)

Solo el rol **Administrador** ve la pestaña **Usuarios**. Permite listar usuarios, agregar (usuario, contraseña, rol, nombre completo), editar (rol, nombre completo, activo y opcionalmente nueva contraseña) y eliminar. Las contraseñas se almacenan con **bcrypt** (máximo 72 bytes). No se puede eliminar al último Administrador.

**Ubicación:** `services/usuarios_service.py`. Vista: `ui/usuarios_view.py`. Roles: `UsuariosService.listar_roles()`.

| Operación | Método | Archivo | Líneas aprox. |
|-----------|--------|---------|----------------|
| **SELECT – listar todos** (con nombre_rol) | `listar_todos()` | `services/usuarios_service.py` | 26-28 |
| **SELECT – buscar por ID** | `buscar_por_id()` | `services/usuarios_service.py` | 52-55 |
| **INSERT – crear usuario** | `agregar()` | `services/usuarios_service.py` | 107-109 |
| **UPDATE – editar usuario** (rol, nombre, activo, opcional password) | `editar()` | `services/usuarios_service.py` | 133-139 |
| **DELETE – eliminar usuario** | `eliminar()` | `services/usuarios_service.py` | 169 |

---

## 9. Módulo de ventas y transacciones

El módulo de ventas es el proceso central: el usuario selecciona productos, define cantidades, puede asociar un cliente (del catálogo o texto libre), registra la venta y el sistema **descuenta automáticamente** el stock.

**Flujo técnico:**

1. Validar líneas de venta (cantidad > 0, precio ≥ 0, **stock suficiente** por producto).
2. Calcular el total.
3. Abrir conexión y **desactivar autocommit** para usar una transacción explícita.
4. Insertar el encabezado de la venta (total, id_cliente, cliente, observaciones).
5. Para cada línea: insertar en **detalle_ventas** y **actualizar el stock** del producto.
6. Hacer **commit**; en caso de error, **rollback**.
7. Restaurar autocommit y cerrar conexión.

**Consultas representativas:** INSERT en ventas con `id_cliente` y `cliente`; INSERT en detalle_ventas; UPDATE productos SET stock = stock - cantidad. Historial: SELECT de ventas ordenado por fecha_venta DESC.

El uso de **transacción explícita** garantiza que si falla cualquier paso, se hace **rollback** y no quedan ventas sin stock actualizado ni inventario inconsistente.

**Ubicación:** `services/ventas_service.py` (registrar_venta, validar_lineas, historial).

---

## 10. Comunicación entre la interfaz y la base de datos

1. El usuario hace clic en un botón (Login, Agregar, Guardar, Actualizar, Eliminar, Registrar venta, etc.).
2. La UI recoge los datos del formulario.
3. La capa de **servicios** aplica validaciones y reglas de negocio (incluyendo autenticación y permisos por rol).
4. Los servicios usan **db/conexion** para abrir conexión, ejecutar consultas SQL parametrizadas y cerrar.
5. El resultado vuelve a la interfaz, que actualiza tablas, mensajes o historial.

La interfaz **no ejecuta SQL directamente**; todo pasa por los servicios.

---

## 11. Actualización de la interfaz

Para que el usuario **vea el stock actualizado** después de una venta:

- Al **cambiar a la pestaña Productos** (o Stock), se refresca la lista desde la base de datos (evento `<<NotebookTabChanged>>`).
- Tras **registrar una venta** con éxito, se llama a un callback que actualiza la lista de productos en segundo plano.

Así, los valores de stock mostrados coinciden con la base de datos.

---

## 12. Seguridad y buenas prácticas

- **Consultas parametrizadas:** todos los valores se envían como parámetros (`%s`), nunca concatenados en la cadena SQL, para evitar inyección SQL.
- **Contraseñas:** hash con bcrypt (límite 72 bytes); no se almacenan en texto plano.
- **Roles:** la ventana principal muestra solo las pestañas permitidas para el rol (Administrador o Vendedor).
- **Validaciones en servicios:** nombre no vacío, precios y cantidades no negativos, stock suficiente antes de vender, no eliminar al último Administrador.
- **Transacciones:** el proceso de venta se ejecuta dentro de una transacción con commit/rollback para mantener consistencia.

---

## 13. Conclusión técnica

OmniStock integra **Python**, diseño modular por capas, **MySQL**, consultas SQL parametrizadas, **login con roles** (Administrador y Vendedor), **gestión de usuarios y clientes**, **transacciones** en ventas y actualización coherente de la interfaz. Desde el punto de vista académico, el proyecto demuestra uso de estructuras de software, conexión a datos, autenticación, autorización por roles, validación, lógica de negocio y capacidad de explicar el código de forma técnica.

---

## 14. Guion de exposición dividido en 3 personas

Propuesta para un video de **6 a 10 minutos**. Cada persona explica **una de las tres capas** del sistema (presentación, lógica de negocio, datos), aparece en cámara y muestra pantalla.

---

### Persona 1 — Capa de presentación (UI)

**Qué debe explicar:** Formularios, tablas, botones y ventanas con Tkinter/ttk. Login y ventana principal según rol (Administrador: Productos, Clientes, Ventas, Usuarios; Vendedor: Stock, Clientes, Ventas). Toda esta capa está en la carpeta **ui/**.

**Archivos que debe abrir y en qué orden (ruta desde la raíz del proyecto):**

1. **ui/login_view.py** — Ventana de login: formulario con campos Usuario y Contraseña, botones Iniciar sesión y Salir. Aquí se capturan las credenciales; al validar, esta ventana se cierra y se abre la ventana principal.
2. **ui/main_window.py** — Ventana principal con pestañas (notebook). Según el rol del usuario se agregan las pestañas: Administrador → Productos, Clientes, Ventas, Usuarios; Vendedor → Stock, Clientes, Ventas. Aquí se instancian las vistas.
3. **ui/productos_view.py** — Formulario y tabla de productos (nombre, descripción, precio, stock), botones Buscar, Limpiar, Nuevo, Guardar, Actualizar, Eliminar. Para Vendedor la misma vista se usa en modo solo lectura (solo tabla y búsqueda).
4. **ui/clientes_view.py** — Formulario y tabla de clientes (nombre, documento, teléfono, email, dirección), botones de CRUD.
5. **ui/ventas_view.py** — Interfaz de ventas: selección de productos, cantidades, cliente opcional, botón Registrar venta, historial de ventas.
6. **ui/usuarios_view.py** — Solo visible para Administrador: tabla de usuarios (usuario, rol, nombre completo, activo), formulario y botones Nuevo, Guardar, Actualizar, Eliminar.

**Guion a leer (ajustar nombre y carrera):**

*"Buenos días. Mi nombre es [Nombre completo], estudiante de [carrera], y voy a explicar la **capa de presentación** de OmniStock."*

*"Todos los elementos que el usuario ve están en la carpeta **ui**. Abro **ui/login_view.py**: aquí está la ventana de login con formulario y botones en Tkinter/ttk. Al iniciar sesión correctamente, esta ventana se cierra y se abre la ventana principal."*

*"La ventana principal está en **ui/main_window.py**: es la que muestra las pestañas. Si el usuario es Administrador, ve Productos, Clientes, Ventas y Usuarios. Si es Vendedor, ve solo Stock, Clientes y Ventas. Cada pestaña es una vista: **ui/productos_view.py** tiene la tabla y formulario de productos; **ui/clientes_view.py** la de clientes; **ui/ventas_view.py** el registro de ventas; **ui/usuarios_view.py** la gestión de usuarios, solo para Admin. Todo lo visual —formularios, tablas y botones— está en estos archivos dentro de **ui/** y se construye con Tkinter y ttk."*

**Mostrar en pantalla (en este orden):** 1) Carpeta **ui/** en el explorador de archivos. 2) Archivo **ui/login_view.py** abierto en el editor. 3) Aplicación ejecutándose: ventana de login, luego ventana principal con pestañas (mostrar como Admin y como Vendedor si se puede). 4) **ui/main_window.py**, **ui/productos_view.py**, **ui/clientes_view.py** abiertos para señalar dónde están formularios y tablas.

---

### Persona 2 — Capa de lógica de negocio (services)

**Qué debe explicar:** Validaciones, reglas de stock, proceso de ventas, autenticación (bcrypt), CRUD de productos, clientes y usuarios. Los servicios son el puente entre la UI y la base de datos. Toda esta capa está en la carpeta **services/**.

**Archivos que debe abrir y en qué orden (ruta desde la raíz del proyecto):**

1. **services/auth_service.py** — Autenticación: login con usuario y contraseña, hash y verificación con **bcrypt**. Creación del usuario admin por defecto si no hay usuarios. Métodos: `login()`, `_hash_password()`, `_check_password()`.
2. **services/inventario_service.py** — CRUD de productos: listar, buscar por ID, buscar por texto, agregar, editar, eliminar. Validaciones: nombre no vacío, precio y stock no negativos. Clase **InventarioService**.
3. **services/clientes_service.py** — CRUD de clientes: listar, buscar por ID, buscar por texto, agregar, editar, eliminar. Validación: nombre no vacío. Clase **ClientesService**.
4. **services/usuarios_service.py** — CRUD de usuarios (solo para Administrador): listar, agregar, editar, eliminar; listar roles. Contraseñas con bcrypt. No se puede eliminar al último Administrador. Clase **UsuariosService**.
5. **services/ventas_service.py** — Proceso de ventas: validar líneas (cantidad, precio, **stock suficiente**), calcular total, registrar venta en transacción (INSERT venta, INSERT detalle, UPDATE stock). Métodos: `validar_lineas()`, `registrar_venta()`, historial. Clase **VentasService**.

**Guion a leer (ajustar nombre y carrera):**

*"Hola, mi nombre es [Nombre completo] y voy a explicar la **capa de lógica de negocio**."*

*"Todos los servicios están en la carpeta **services**. Abro **services/auth_service.py**: aquí está la autenticación con **bcrypt** —hash y verificación de contraseña— y el login. Siguiente: **services/inventario_service.py** —CRUD de productos y validaciones como nombre no vacío y precios no negativos. **services/clientes_service.py** —CRUD de clientes. **services/usuarios_service.py** —CRUD de usuarios y roles, contraseñas con bcrypt. Por último, **services/ventas_service.py**: aquí están las **reglas de stock** —validar que haya stock suficiente— y el **proceso de ventas** completo en transacción: insertar venta, detalle y descontar stock."*

*"Esta capa no dibuja pantallas; recibe datos de la interfaz, aplica validaciones y reglas, y llama a la base de datos. Los archivos son: **auth_service.py**, **inventario_service.py**, **clientes_service.py**, **usuarios_service.py** y **ventas_service.py**, todos dentro de **services/**."*

**Mostrar en pantalla (en este orden):** 1) Carpeta **services/** en el explorador. 2) **services/auth_service.py** — señalar uso de bcrypt. 3) **services/inventario_service.py** — señalar validaciones y métodos CRUD. 4) **services/ventas_service.py** — señalar `validar_lineas`, `registrar_venta` y transacción (autocommit False, commit/rollback).

---

### Persona 3 — Capa de datos

**Qué debe explicar:** Entorno MySQL (Wampserver, MySQL 8.4.7). Conexión a MySQL desde el proyecto (config.py, db/conexion.py), ejecución de consultas parametrizadas (%s), modelos (Producto, Venta, DetalleVenta, Cliente, Usuario, Rol). La configuración y la conexión están en la raíz y en **db/**; los modelos en **models/**.

**Antes de abrir archivos del proyecto — Servidor MySQL (Wampserver):**

- En la **bandeja del sistema** (system tray), localizar el icono de **Wampserver** (W).
- Clic izquierdo o derecho sobre el icono: verificar que **MySQL** esté en verde (en ejecución) y que figure como motor por defecto **MySQL 8.4.7** (no MariaDB). Si no está en marcha: **Start All Services** o iniciar solo el servicio MySQL.
- Opcional: desde el menú de Wampserver, **MySQL** → **my.ini** para mostrar dónde se configura el servidor (puerto 3306, etc.). La aplicación OmniStock se conecta a ese MySQL en localhost.

**Archivos que debe abrir y en qué orden (ruta desde la raíz del proyecto):**

1. **config.py** — En la **raíz del proyecto**. Diccionario **DB_CONFIG** con host (localhost), user (root), password, database (omnistock), charset, autocommit. Aquí se define a qué MySQL se conecta la aplicación (el que corre en Wampserver).
2. **db/conexion.py** — Funciones **obtener_conexion()** y **cerrar_conexion(conexion)**. Todas las consultas usan estas funciones para abrir y cerrar la conexión.
3. **models/productos.py** — Modelo **Producto** (id, nombre, descripcion, precio, stock, fecha_creacion, fecha_actualizacion).
4. **models/ventas.py** — Modelos **Venta** (id, fecha_venta, total, id_cliente, cliente, observaciones) y **DetalleVenta** (id, id_venta, id_producto, cantidad, precio_unitario, subtotal).
5. **models/cliente.py** — Modelo **Cliente** (id, nombre, documento, telefono, email, direccion, fecha_creacion).
6. **models/usuario.py** — Modelos **Rol** (id, nombre) y **Usuario** (id, usuario, id_rol, nombre_rol, nombre_completo, activo).

Para mostrar **consultas parametrizadas** (placeholders %s), abrir por ejemplo **services/inventario_service.py** (líneas del SELECT, INSERT, UPDATE, DELETE con %s) o **services/ventas_service.py** (INSERT ventas, INSERT detalle_ventas, UPDATE productos).

**Guion a leer (ajustar nombre y carrera):**

*"Hola, mi nombre es [Nombre completo] y voy a explicar la **capa de datos**."*

*"El servidor MySQL que usamos corre con **Wampserver**. Muestro el icono en la bandeja del sistema: MySQL debe estar en verde; en nuestro caso es **MySQL 8.4.7**. La aplicación se conecta a ese servidor en localhost. La configuración del servidor está en **my.ini**, que se abre desde el menú de Wampserver, MySQL."*

*"En el proyecto, la **conexión** se define en **config.py**, en la raíz: el diccionario DB_CONFIG con host localhost, usuario root, base de datos omnistock, etc. La conexión real se obtiene y se cierra en **db/conexion.py** —funciones obtener_conexion y cerrar_conexion. Todos los servicios usan este archivo para conectar al MySQL de Wampserver."*

*"Los **modelos** están en la carpeta **models**. Abro **models/productos.py** —clase Producto. **models/ventas.py** —clases Venta y DetalleVenta. **models/cliente.py** —clase Cliente. **models/usuario.py** —clases Rol y Usuario. Cada fila que viene de MySQL se convierte en un objeto de estos modelos."*

*"Todas las consultas son **parametrizadas**: se usan placeholders **%s** y los valores se pasan aparte, nunca concatenados en el SQL. Pueden verlo en **services/inventario_service.py** —por ejemplo el INSERT o el UPDATE— o en **services/ventas_service.py** en el INSERT de ventas y el UPDATE de stock. Así se evita la inyección SQL."*

**Mostrar en pantalla (en este orden):** 1) **Wampserver** en la bandeja del sistema: mostrar que MySQL está en ejecución (verde) y que el DBMS por defecto es MySQL 8.4.7. Opcional: menú Wampserver → MySQL → **my.ini**. 2) **config.py** (raíz). 3) **db/conexion.py**. 4) Carpeta **models/** y archivos **models/productos.py**, **models/ventas.py**, **models/cliente.py**, **models/usuario.py** abiertos para señalar cada clase. 5) **services/inventario_service.py** o **services/ventas_service.py** con el cursor abierto en una línea que use **%s** en la consulta.

---

## 15. Recomendaciones para la grabación

- Hablar de forma clara y pausada mientras se muestra el sistema.
- No limitarse a mostrar botones; explicar qué hace el código y qué consulta se ejecuta.
- Aparecer en cámara al inicio de cada intervención con nombre, asignatura y carrera.
- Mostrar el código real en el editor que usaron (VS Code, PyCharm, etc.).
- Relacionar cada acción de la interfaz con su impacto en MySQL y con el rol (Admin vs Vendedor).
- Cerrar con una reflexión breve sobre aprendizajes técnicos y trabajo en equipo.

---

## 16. Frases útiles

- *"Aquí observamos el punto de entrada del sistema y el flujo de login."*
- *"Tras validar usuario y contraseña con bcrypt, se cierra el login y se abre la ventana principal según el rol."*
- *"El servidor MySQL corre con Wampserver; usamos MySQL 8.4.7 como motor por defecto."*
- *"En config.py se define la configuración de conexión a MySQL (localhost, usuario, base omnistock)."*
- *"Esta consulta SELECT carga los productos en la interfaz."*
- *"El Vendedor solo ve la pestaña Stock para consultar cantidades; no puede modificar productos."*
- *"En ventas usamos una transacción explícita: commit si todo va bien, rollback si hay error."*
- *"Con este UPDATE descontamos el stock después de la venta."*
- *"El Administrador puede gestionar usuarios en la pestaña Usuarios; las contraseñas se guardan con bcrypt."*
- *"Al cambiar a la pestaña Productos o Stock, la lista se refresca para mostrar el stock actualizado."*
- *"Este flujo evidencia la comunicación entre la interfaz, los servicios y la base de datos."*

---

*Documento alineado con el código del proyecto OmniStock (Python, Tkinter, MySQL, login con roles, CRUD productos, clientes y usuarios).*
