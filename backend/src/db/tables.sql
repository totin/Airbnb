-- =====================================================================
-- Proyecto 1 — Airbnb
-- =====================================================================

DROP DATABASE IF EXISTS airbnb;
CREATE DATABASE airbnb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE airbnb;

-- =====================================================================
-- Tabla: usuario
-- =====================================================================
CREATE TABLE usuario (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    email           VARCHAR(150) NOT NULL UNIQUE,
    nombre          VARCHAR(100) NOT NULL,
    fecha_registro  DATE NOT NULL DEFAULT (CURRENT_DATE),
    es_anfitrion    BOOLEAN NOT NULL DEFAULT FALSE
) ENGINE=InnoDB;

-- =====================================================================
-- Tabla: propiedad
-- =====================================================================
CREATE TABLE propiedad (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    titulo          VARCHAR(150) NOT NULL,
    direccion       VARCHAR(200) NOT NULL,
    ciudad          VARCHAR(100) NOT NULL,
    precio_noche    DECIMAL(10,2) NOT NULL,
    capacidad       INT NOT NULL,
    anfitrion_id    INT NOT NULL,
    CONSTRAINT fk_propiedad_anfitrion
        FOREIGN KEY (anfitrion_id) REFERENCES usuario(id)
        ON DELETE CASCADE,
    CONSTRAINT chk_precio_noche CHECK (precio_noche > 0),
    CONSTRAINT chk_capacidad CHECK (capacidad > 0)
) ENGINE=InnoDB;

CREATE INDEX idx_propiedad_ciudad ON propiedad(ciudad);

-- =====================================================================
-- Tabla: reserva
-- =====================================================================

CREATE TABLE reserva (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    propiedad_id    INT NOT NULL,
    huesped_id      INT NOT NULL,
    fecha_inicio    DATE NOT NULL,
    fecha_fin       DATE NOT NULL,
    estado          ENUM('pendiente', 'confirmada', 'cancelada', 'finalizada')
                        NOT NULL DEFAULT 'pendiente',
    total           DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_reserva_propiedad
        FOREIGN KEY (propiedad_id) REFERENCES propiedad(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reserva_huesped
        FOREIGN KEY (huesped_id) REFERENCES usuario(id)
        ON DELETE CASCADE,
    CONSTRAINT chk_fechas_reserva CHECK (fecha_fin > fecha_inicio),
    CONSTRAINT chk_total CHECK (total >= 0)
) ENGINE=InnoDB;

CREATE INDEX idx_reserva_fechas ON reserva(fecha_inicio, fecha_fin);

-- =====================================================================
-- Tabla: resena
-- =====================================================================
CREATE TABLE resena (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id      INT NOT NULL UNIQUE,
    autor_id        INT NOT NULL,
    puntaje         INT NOT NULL,
    comentario      TEXT,
    fecha           DATE NOT NULL DEFAULT (CURRENT_DATE),
    CONSTRAINT fk_resena_reserva
        FOREIGN KEY (reserva_id) REFERENCES reserva(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_resena_autor
        FOREIGN KEY (autor_id) REFERENCES usuario(id)
        ON DELETE CASCADE,
    CONSTRAINT chk_puntaje CHECK (puntaje BETWEEN 1 AND 5)
) ENGINE=InnoDB;

-- =====================================================================
-- Tabla: amenidad
-- =====================================================================
CREATE TABLE amenidad (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    nombre  VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- =====================================================================
-- Relación N a M: propiedad_amenidades
-- =====================================================================
CREATE TABLE propiedad_amenidades (
    propiedad_id    INT NOT NULL,
    amenidad_id     INT NOT NULL,
    PRIMARY KEY (propiedad_id, amenidad_id),
    CONSTRAINT fk_pa_propiedad
        FOREIGN KEY (propiedad_id) REFERENCES propiedad(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_pa_amenidad
        FOREIGN KEY (amenidad_id) REFERENCES amenidad(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- =====================================================================
-- Relación N a M: favoritos
-- =====================================================================
CREATE TABLE favoritos (
    usuario_id      INT NOT NULL,
    propiedad_id    INT NOT NULL,
    fecha           DATE NOT NULL DEFAULT (CURRENT_DATE),
    PRIMARY KEY (usuario_id, propiedad_id),
    CONSTRAINT fk_fav_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_fav_propiedad
        FOREIGN KEY (propiedad_id) REFERENCES propiedad(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- =====================================================================
-- Fin del script
-- =====================================================================