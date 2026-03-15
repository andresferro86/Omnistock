-- ============================================================
-- OmniStock - Script de base de datos MySQL
-- Sistema de Gestión de Inventario y Ventas
-- Moneda: todos los importes están en PESOS (MXN/COP, etc.)
-- Ejecutar en MySQL (Workbench, línea de comandos o cliente)
-- ============================================================

-- Crear y usar la base de datos
CREATE DATABASE IF NOT EXISTS omnistock
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE omnistock;

-- ============================================================
-- Tabla: productos
-- Catálogo de productos con precio (en pesos) y stock
-- ============================================================
CREATE TABLE IF NOT EXISTS productos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(200) NOT NULL,
  descripcion VARCHAR(500) DEFAULT NULL,
  precio DECIMAL(12, 2) NOT NULL COMMENT 'Precio en pesos' CHECK (precio >= 0),
  stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_nombre (nombre),
  INDEX idx_stock (stock)
) ENGINE=InnoDB;

-- ============================================================
-- Tabla: ventas
-- Cabecera de cada venta (fecha y total en pesos)
-- ============================================================
CREATE TABLE IF NOT EXISTS ventas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  fecha_venta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total DECIMAL(12, 2) NOT NULL DEFAULT 0.00 COMMENT 'Total en pesos' CHECK (total >= 0),
  cliente VARCHAR(200) DEFAULT NULL,
  observaciones VARCHAR(500) DEFAULT NULL,
  INDEX idx_fecha (fecha_venta)
) ENGINE=InnoDB;

-- ============================================================
-- Tabla: detalle_ventas
-- Líneas de cada venta (producto, cantidad, precio unitario en pesos)
-- ============================================================
CREATE TABLE IF NOT EXISTS detalle_ventas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_venta INT NOT NULL,
  id_producto INT NOT NULL,
  cantidad INT NOT NULL CHECK (cantidad > 0),
  precio_unitario DECIMAL(12, 2) NOT NULL COMMENT 'Precio unitario en pesos' CHECK (precio_unitario >= 0),
  subtotal DECIMAL(12, 2) NOT NULL COMMENT 'Subtotal en pesos' CHECK (subtotal >= 0),
  CONSTRAINT fk_detalle_venta FOREIGN KEY (id_venta) REFERENCES ventas(id) ON DELETE CASCADE,
  CONSTRAINT fk_detalle_producto FOREIGN KEY (id_producto) REFERENCES productos(id),
  INDEX idx_venta (id_venta),
  INDEX idx_producto (id_producto)
) ENGINE=InnoDB;

-- ============================================================
-- Datos de prueba (INSERT) - Precios en pesos
-- ============================================================

INSERT INTO productos (nombre, descripcion, precio, stock) VALUES
('Lápiz HB', 'Lápiz grafito grado HB', 15.00, 100),
('Cuaderno cuadriculado', 'Cuaderno 100 hojas', 32.00, 80),
('Borrador', 'Borrador blanco estándar', 8.00, 150),
('Regla 30 cm', 'Regla plástica transparente', 20.00, 60),
('Pegamento en barra', 'Pegamento 40 g', 25.00, 45),
('Tijeras escolares', 'Tijeras punta redonda', 40.00, 30),
('Resaltador amarillo', 'Marcador resaltador', 28.00, 70),
('Grapadora', 'Grapadora metálica', 85.00, 25);

-- Una venta de ejemplo con dos productos (importes en pesos)
INSERT INTO ventas (fecha_venta, total, cliente, observaciones) VALUES
(NOW(), 0.00, 'Cliente prueba', 'Venta de ejemplo');

SET @id_venta_ejemplo = LAST_INSERT_ID();

INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, precio_unitario, subtotal) VALUES
(@id_venta_ejemplo, 1, 5, 15.00, 75.00),
(@id_venta_ejemplo, 2, 2, 32.00, 64.00);

UPDATE ventas SET total = 139.00 WHERE id = @id_venta_ejemplo;

-- Descontar stock de los productos vendidos en la venta de ejemplo
UPDATE productos SET stock = stock - 5 WHERE id = 1;
UPDATE productos SET stock = stock - 2 WHERE id = 2;

-- ============================================================
-- Fin del script
-- ============================================================
