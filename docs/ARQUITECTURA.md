# OmniStock - Arquitectura del Proyecto

## 1. Arquitectura propuesta

Se utiliza una **arquitectura en capas** (presentación → lógica de negocio → datos), adecuada para un proyecto académico:

- **Capa de presentación (UI):** Ventanas Tkinter que muestran formularios y listados; no contienen lógica de negocio.
- **Capa de servicios:** Reglas de negocio, validaciones y orquestación entre modelos y base de datos.
- **Capa de datos:** Conexión a MySQL y modelos que representan las entidades (productos, ventas).

Flujo: el usuario interactúa con la UI → la UI llama a los servicios → los servicios usan la conexión y los modelos para leer/escribir en MySQL.

---

## 2. Estructura de carpetas y archivos

```
OmniStock/
├── main.py                 # Punto de entrada; lanza la aplicación
├── config.py               # Configuración (BD, constantes)
├── requirements.txt        # Dependencias Python
├── README.md               # Instalación y ejecución
├── docs/
│   └── ARQUITECTURA.md     # Este documento
├── database/
│   └── schema.sql          # Script SQL completo (CREATE DB, tablas, datos prueba)
├── db/
│   └── conexion.py         # Gestión de conexión a MySQL
├── models/
│   ├── __init__.py
│   ├── productos.py        # Modelo/entidad Producto
│   └── ventas.py           # Modelo/entidad Venta y DetalleVenta
├── services/
│   ├── __init__.py
│   ├── inventario_service.py   # CRUD productos, validaciones
│   └── ventas_service.py       # Registrar venta, descontar stock, historial
├── ui/
│   ├── __init__.py
│   ├── main_window.py      # Ventana principal con menú/módulos
│   ├── productos_view.py   # Pantalla de productos (listar, agregar, editar, eliminar)
│   └── ventas_view.py      # Pantalla de ventas (registrar, historial)
└── utils/
    ├── __init__.py
    └── helpers.py          # Funciones auxiliares (validar número, mensajes)
```

---

## 3. Función de cada archivo

| Archivo | Función |
|---------|---------|
| **main.py** | Inicia la app, carga configuración y abre la ventana principal. |
| **config.py** | Parámetros de conexión a MySQL (host, usuario, contraseña, base de datos). |
| **db/conexion.py** | Obtiene y cierra la conexión a MySQL; centraliza el acceso a la BD. |
| **models/productos.py** | Define la estructura de un producto (id, nombre, precio, stock, etc.). |
| **models/ventas.py** | Define venta y detalle de venta (cabecera + ítems). |
| **services/inventario_service.py** | Alta, listado, búsqueda, edición y baja de productos; validaciones de negocio. |
| **services/ventas_service.py** | Registrar venta, descontar stock, consultar historial; valida stock suficiente. |
| **ui/main_window.py** | Ventana principal con pestañas o botones para Productos y Ventas. |
| **ui/productos_view.py** | Formulario y tabla de productos; delega en inventario_service. |
| **ui/ventas_view.py** | Formulario de nueva venta y listado de historial; delega en ventas_service. |
| **utils/helpers.py** | Validar números, mostrar mensajes (messagebox), formatear precios. |
| **database/schema.sql** | Crear base de datos, tablas y datos de prueba. |

---

## 4. Modelo de base de datos

- **productos:** catálogo de productos (id, nombre, descripción, precio, stock, fechas).
- **ventas:** cabecera de cada venta (id, fecha, total, cliente opcional).
- **detalle_ventas:** líneas de cada venta (producto, cantidad, precio unitario, subtotal); relación N:1 con ventas y N:1 con productos.

---

## 5. Tablas necesarias

| Tabla | Descripción |
|-------|-------------|
| **productos** | Almacena cada producto con nombre, precio, stock. |
| **ventas** | Una fila por venta (fecha, total). |
| **detalle_ventas** | Una fila por cada producto vendido en una venta (id_venta, id_producto, cantidad, precio_unitario). |

---

## 6. Relaciones entre tablas

- **ventas** 1 — N **detalle_ventas:** una venta tiene varios ítems (FK: detalle_ventas.id_venta → ventas.id).
- **productos** 1 — N **detalle_ventas:** un producto puede aparecer en muchos detalles (FK: detalle_ventas.id_producto → productos.id).

---

## 7. Reglas de negocio principales

1. No permitir ventas con stock insuficiente.
2. No permitir cantidades ni precios negativos.
3. No guardar productos con nombre vacío.
4. Al registrar una venta, descontar automáticamente el stock de cada producto.
5. Validar campos obligatorios antes de guardar (nombre, precio, stock en productos; cantidad y producto en detalle).
6. Mostrar mensajes claros de éxito y error al usuario.
