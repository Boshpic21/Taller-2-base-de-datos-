CREATE DATABASE IF NOT EXISTS bufete_db CHARACTER SET utf8mb4;
USE bufete_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,  
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE aseguradoras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE juzgados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL UNIQUE
);


CREATE TABLE expedientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente VARCHAR(150) NOT NULL,
    aseguradora_id INT NOT NULL,
    juzgado_id INT NOT NULL,
    estado ENUM('pendiente','en_curso','cerrado') NOT NULL DEFAULT 'pendiente',
    fecha_audiencia DATE,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (aseguradora_id) REFERENCES aseguradoras(id),
    FOREIGN KEY (juzgado_id) REFERENCES juzgados(id)
);


INSERT INTO aseguradoras (nombre) VALUES
('ASSA'),
('ANCON'),
('CONANCE'),
('PARTICULAR'),
('INTEROCEANICA');

INSERT INTO juzgados (nombre) VALUES
('JUZGADO 1RO (PEDREGAL)'),
('JUZGADO 3RO (PEDREGAL)'),
('JUZGADO 4TO (PEDREGAL)'),
('JUZGADO 5TO (PEDREGAL)'),
('ALCALDIA DE PANAMA'),
('CHITRE');

INSERT INTO expedientes (cliente, aseguradora_id, juzgado_id, estado, fecha_audiencia) VALUES
('ANTHONY TREJOS',       1, 4, 'pendiente', '2019-01-07'),
('LUIS MOLINA',          2, 3, 'en_curso',  '2019-01-07'),
('KATHERINE KENT',       1, 4, 'pendiente', '2019-01-07'),
('MARTIN ALVARADO',      3, 1, 'cerrado',   '2019-01-07'),
('JOEL ARAUZ RODRIGUEZ', 4, 2, 'en_curso',  '2019-01-07'),
('MICHELLE VEGA',        5, 5, 'pendiente', '2019-01-07'),
('CANDICE HENRY',        2, 6, 'cerrado',   '2019-01-07');
