-- ============================================================
-- Migración: agregar Clientes y Usuarios (para BD ya existentes)
-- Ejecutar solo si ya creó la BD con el schema anterior sin estas tablas.
-- ============================================================

USE omnistock;

-- Tabla roles
CREATE TABLE IF NOT EXISTS roles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- Tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  id_rol INT NOT NULL,
  nombre_completo VARCHAR(200) DEFAULT NULL,
  activo TINYINT(1) NOT NULL DEFAULT 1,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES roles(id),
  INDEX idx_usuario (usuario)
) ENGINE=InnoDB;

-- Tabla clientes
CREATE TABLE IF NOT EXISTS clientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(200) NOT NULL,
  documento VARCHAR(50) DEFAULT NULL,
  telefono VARCHAR(50) DEFAULT NULL,
  email VARCHAR(120) DEFAULT NULL,
  direccion VARCHAR(300) DEFAULT NULL,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_nombre (nombre)
) ENGINE=InnoDB;

-- Agregar columna id_cliente a ventas (solo si su BD se creó con schema antiguo sin esta columna).
-- Si aparece error "Duplicate column name" es que ya tiene la columna; puede omitir estas líneas.
ALTER TABLE ventas ADD COLUMN id_cliente INT DEFAULT NULL AFTER total;
ALTER TABLE ventas ADD CONSTRAINT fk_venta_cliente FOREIGN KEY (id_cliente) REFERENCES clientes(id);
ALTER TABLE ventas ADD INDEX idx_id_cliente (id_cliente);

-- Datos iniciales (ejecutar una sola vez; si da error de duplicado, omitir)
INSERT IGNORE INTO roles (id, nombre) VALUES (1, 'Administrador'), (2, 'Vendedor');
INSERT IGNORE INTO clientes (id, nombre, documento, telefono, email) VALUES
(1, 'Cliente prueba', 'CC 123456', '3001112233', 'cliente@ejemplo.com'),
(2, 'María García', 'CC 654321', '3102223344', 'maria@ejemplo.com');

-- El usuario admin se crea al iniciar la aplicación (contraseña: admin).
