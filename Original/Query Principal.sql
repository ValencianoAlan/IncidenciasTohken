Use Prueba_6

CREATE TABLE usuarios (
    numNomina INT PRIMARY KEY,  -- Cambiamos idUsuario por numNomina (no autoincrementable)
    nombre NVARCHAR(100) NOT NULL,
    apellidoPaterno NVARCHAR(100),
    apellidoMaterno NVARCHAR(100)
);

CREATE TABLE credenciales (
    idCredencial INT IDENTITY(1,1) PRIMARY KEY,  -- Auto-incrementable
    numNomina INT NOT NULL,  -- Cambiamos idUsuario por numNomina
    username NVARCHAR(50) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL,
    FOREIGN KEY (numNomina) REFERENCES usuarios(numNomina)
);

CREATE TABLE roles (
    idRol INT IDENTITY(1,1) PRIMARY KEY,
    nombreRol NVARCHAR(50) NOT NULL UNIQUE  -- Ej: 'Admin', 'Usuario'
);

CREATE TABLE usuario_rol (
    numNomina INT NOT NULL,
    idRol INT NOT NULL,
    PRIMARY KEY (numNomina, idRol),
    FOREIGN KEY (numNomina) REFERENCES usuarios(numNomina),
    FOREIGN KEY (idRol) REFERENCES roles(idRol)
);

CREATE TABLE puestos (
    idPuesto INT IDENTITY(1,1) PRIMARY KEY,  -- Auto-incrementable
    nombrePuesto NVARCHAR(100) NOT NULL UNIQUE  -- Nombre del puesto
);

-- Tabla para relacionar usuarios con puestos
CREATE TABLE usuario_puesto (
    numNomina INT NOT NULL,
    idPuesto INT NOT NULL,
    PRIMARY KEY (numNomina, idPuesto),
    FOREIGN KEY (numNomina) REFERENCES usuarios(numNomina),
    FOREIGN KEY (idPuesto) REFERENCES puestos(idPuesto)
);

CREATE TABLE departamentos (
    idDepartamento INT IDENTITY(1,1) PRIMARY KEY,  -- Auto-incrementable
    nombreDepartamento NVARCHAR(100) NOT NULL UNIQUE  -- Nombre del departamento
);

CREATE TABLE departamento_puesto (
    idDepartamento INT NOT NULL,
    idPuesto INT NOT NULL,
    PRIMARY KEY (idDepartamento, idPuesto),
    FOREIGN KEY (idDepartamento) REFERENCES departamentos(idDepartamento),
    FOREIGN KEY (idPuesto) REFERENCES puestos(idPuesto)
);

-- Crear la tabla de motivos de incidencias
CREATE TABLE motivos (
    idMotivo INT IDENTITY(1,1) PRIMARY KEY, -- Clave primaria autoincremental
    nombreMotivo NVARCHAR(100) NOT NULL -- Nombre del motivo (ej: Vacaciones, Permiso, etc.)
);

-- Crear la tabla de incidencias
CREATE TABLE incidencias (
    idIncidencia INT IDENTITY(1,1) PRIMARY KEY, -- Clave primaria autoincremental
    numNomina INT NOT NULL, -- Número de nómina del usuario que realiza la incidencia
    idMotivo INT NOT NULL, -- Motivo de la incidencia
    fechaSolicitud DATE NOT NULL DEFAULT GETDATE(), -- Fecha de solicitud (automática)
    fechaInicio DATE NOT NULL, -- Fecha de inicio de la incidencia
    fechaFin DATE NOT NULL, -- Fecha de fin de la incidencia
    numDias INT, -- Número de días (se calculará automáticamente)
    comentarios NVARCHAR(500), -- Comentarios adicionales
    FOREIGN KEY (numNomina) REFERENCES usuarios(numNomina), -- Relación con la tabla usuarios
    FOREIGN KEY (idMotivo) REFERENCES motivos(idMotivo) -- Relación con la tabla motivos
);


select * from credenciales;
select * from roles;
select * from usuario_rol;
select * from usuarios;
select * from puestos order by idPuesto;
select * from departamentos ORDER BY idDepartamento;
select * from departamento_puesto;

INSERT INTO roles (nombreRol) VALUES ('Admin'), ('Usuario');
insert into usuarios (numNomina,nombre,apellidoPaterno,apellidoMaterno)
values (1035,'Alan de Jesús','Valenciano','Llamas');

Insert into credenciales (numNomina,username,password)
values(1035,'alan.valenciano','12345');

insert into usuario_rol (numNomina,idRol)
values (1035,1);

SELECT u.numNomina, u.nombre, r.nombreRol
FROM usuarios u
INNER JOIN usuario_rol ur ON u.numNomina = ur.numNomina
INNER JOIN roles r ON ur.idRol = r.idRol;

SET IDENTITY_INSERT roles ON

INSERT INTO roles (idRol,nombreRol) VALUES 
(3,'Gerente'),
(4, 'Supervisor')

INSERT INTO departamentos (nombreDepartamento) VALUES
('Administración'),
('Compras'),
('Ventas'),
('Finanzas'),
('Sistemas'),
('Control de Producción'),
('Producción'),
('Mantenimiento'),
('Seguridad e Higiene y Medio Ambiente');

INSERT INTO puestos (nombrePuesto) VALUES
('Director General'),
('Gerente General de Administración'),
('Gerente de Planta'),
('Gerente General de Ventas'),
('Gerente Senior de Finanzas'),
('Gerente'),
('Asistente para el Gerente General de Administración'),
('Asistente de Gerente'),
('Supervisor Senior de APQP'),
('Supervisor Senior de Producción'),
('Supervisor ISO'),
('Supervisor de Atención a Cliente'),
('Supervisor'),
('Traductor'),
('Medico'),
('Lider'),
('Auxiliar'),
('Tecnico'),
('Enfermero(a)'),
('Inspector'),
('Almacenista'),
('Operario');

-- Agregar la columna idDepartamento a la tabla usuarios
ALTER TABLE usuarios
ADD idDepartamento INT;

-- Establecer idDepartamento como clave foránea
ALTER TABLE usuarios
ADD CONSTRAINT fk_usuario_departamento
FOREIGN KEY (idDepartamento) REFERENCES departamentos(idDepartamento);

UPDATE usuarios
SET idDepartamento = 5
WHERE numNomina = 1035;

UPDATE usuarios
SET idDepartamento = 5
WHERE numNomina = 712;

UPDATE usuarios
SET idDepartamento = 1
WHERE numNomina = 1242;

-- Agregar la columna idPuesto a la tabla usuarios
ALTER TABLE usuarios
ADD idPuesto INT;

-- Establecer idPuesto como clave foránea
ALTER TABLE usuarios
ADD CONSTRAINT fk_usuario_puesto
FOREIGN KEY (idPuesto) REFERENCES puestos(idPuesto);

-- Asignar el usuario con numNomina 1242 al puesto con idPuesto 16
UPDATE usuarios
SET idPuesto = 16
WHERE numNomina = 1242;

-- Asignar el usuario con numNomina 712 al puesto con idPuesto 16
UPDATE usuarios
SET idPuesto = 16
WHERE numNomina = 712;

UPDATE usuarios
SET idPuesto = 17
WHERE numNomina = 1035;

select u.nombre as 'Nombre', u.apellidoPaterno as 'Apellido Paterno', d.nombreDepartamento as 'Departamento' , p.nombrePuesto as 'Puesto'
from usuarios u, departamentos d, puestos p
where u.idDepartamento = d.idDepartamento
and u.idPuesto = p.idPuesto

ALTER TABLE puestos
ADD idDepartamento INT;

ALTER TABLE puestos
ADD CONSTRAINT uq_nombrePuesto UNIQUE (nombrePuesto);

ALTER TABLE departamento_puesto
ADD CONSTRAINT fk_departamento
FOREIGN KEY (idDepartamento) REFERENCES departamentos(idDepartamento)
ON DELETE CASCADE;

ALTER TABLE departamento_puesto
ADD CONSTRAINT fk_puesto
FOREIGN KEY (idPuesto) REFERENCES puestos(idPuesto)
ON DELETE CASCADE;

select dp.idDepartamento, d.nombreDepartamento, p.nombrePuesto 
from departamento_puesto dp, departamentos d, puestos p
where dp.idDepartamento = d.idDepartamento
and dp.idPuesto = p.idPuesto

SELECT 
    u.numNomina, 
    u.nombre, 
    u.apellidoPaterno, 
    u.apellidoMaterno, 
    c.username, 
    ur.idRol, 
    u.idDepartamento, 
    u.idPuesto
FROM usuarios u
INNER JOIN credenciales c ON u.numNomina = c.numNomina
INNER JOIN usuario_rol ur ON u.numNomina = ur.numNomina
INNER JOIN departamento_puesto dp ON u.idDepartamento = dp.idDepartamento
AND u.idPuesto = dp.idPuesto
WHERE u.numNomina = 1035

ALTER TABLE usuarios
ADD diasVacaciones INT DEFAULT 0;

UPDATE usuarios
SET diasVacaciones = 7
WHERE numNomina = 1035;

INSERT INTO motivos (nombreMotivo)
VALUES 
('Permiso sin goce de sueldo'),
('Permiso con goce de sueldo'),
('Vacaciones'),
('Olvido de gafete'),
('Tiempo x Tiempo');

select * from motivos

INSERT INTO incidencias (numNomina, idMotivo, fechaInicio, fechaFin, comentarios)
VALUES 
(1035, 3, '2023-10-01', '2023-10-05', 'Vacaciones de verano');

SELECT i.idIncidencia, u.nombre, m.nombreMotivo, i.fechaSolicitud, i.fechaInicio, i.fechaFin, i.numDias, i.comentarios
FROM incidencias i
JOIN usuarios u ON i.numNomina = u.numNomina
JOIN motivos m ON i.idMotivo = m.idMotivo
WHERE u.numNomina = 1035;

SELECT diasVacaciones
FROM usuarios
WHERE numNomina = 1035;

CREATE TRIGGER calcular_dias_incidencia
ON incidencias
AFTER INSERT, UPDATE
AS
BEGIN
    UPDATE incidencias
    SET numDias = DATEDIFF(DAY, fechaInicio, fechaFin) + 1
    WHERE idIncidencia IN (SELECT idIncidencia FROM inserted);
END;

INSERT INTO incidencias (numNomina, idMotivo, fechaInicio, fechaFin, comentarios)
VALUES 
(1035, 3, '2023-10-01', '2023-10-05', 'Vacaciones de verano');

SELECT * from incidencias where numNomina=1035;

UPDATE incidencias
SET fechaInicio = '2023-10-02', fechaFin = '2023-10-06'
WHERE idIncidencia = 1;

SELECT idIncidencia, numNomina, idMotivo, fechaSolicitud, fechaInicio, fechaFin, numDias, comentarios
FROM incidencias;

DISABLE TRIGGER calcular_dias_incidencia ON incidencias;
DROP TRIGGER calcular_dias_incidencia;

CREATE TRIGGER calcular_dias_incidencia
ON incidencias
AFTER INSERT, UPDATE
AS
BEGIN
    -- Calcular el número de días de la incidencia
    UPDATE incidencias
    SET numDias = DATEDIFF(DAY, fechaInicio, fechaFin) + 1
    WHERE idIncidencia IN (SELECT idIncidencia FROM inserted);

    -- Restar los días de vacaciones si el motivo es "Vacaciones"
    UPDATE usuarios
    SET diasVacaciones = diasVacaciones - i.numDias
    FROM usuarios u
    INNER JOIN inserted i ON u.numNomina = i.numNomina
    INNER JOIN motivos m ON i.idMotivo = m.idMotivo
    WHERE m.nombreMotivo = 'Vacaciones';
END;


SELECT numNomina, nombre, diasVacaciones
FROM usuarios
WHERE numNomina = 1035;

INSERT INTO incidencias (numNomina, idMotivo, fechaInicio, fechaFin, comentarios)
VALUES 
(1035, 3, '2025-03-05', '2025-03-10', 'Vacaciones de verano');

DROP TRIGGER calcular_dias_incidencia;

truncate table incidencias

CREATE PROCEDURE crear_incidencia
    @numNomina INT,
    @idMotivo INT,
    @fechaInicio DATE,
    @fechaFin DATE,
    @comentarios NVARCHAR(500)
AS
BEGIN
    -- Calcular el número de días
    DECLARE @numDias INT;
    SET @numDias = DATEDIFF(DAY, @fechaInicio, @fechaFin) + 1;

    -- Validar si el motivo es vacaciones (idMotivo = 3)
    IF @idMotivo = 3
    BEGIN
        -- Verificar si el usuario tiene suficientes días de vacaciones
        IF (SELECT diasVacaciones FROM usuarios WHERE numNomina = @numNomina) >= @numDias
        BEGIN
            -- Restar los días de vacaciones
            UPDATE usuarios
            SET diasVacaciones = diasVacaciones - @numDias
            WHERE numNomina = @numNomina;
|
            -- Insertar la incidencia
            INSERT INTO incidencias (numNomina, idMotivo, fechaSolicitud, fechaInicio, fechaFin, numDias, comentarios)
            VALUES (@numNomina, @idMotivo, GETDATE(), @fechaInicio, @fechaFin, @numDias, @comentarios);
        END
        ELSE
        BEGIN
            -- Lanzar un error si no hay suficientes días de vacaciones
            RAISERROR('No tienes suficientes días de vacaciones disponibles.', 16, 1);
        END
    END
    ELSE
    BEGIN
        -- Insertar la incidencia si no es vacaciones
        INSERT INTO incidencias (numNomina, idMotivo, fechaSolicitud, fechaInicio, fechaFin, numDias, comentarios)
        VALUES (@numNomina, @idMotivo, GETDATE(), @fechaInicio, @fechaFin, @numDias, @comentarios);
    END
END;

EXEC crear_incidencia 
    @numNomina = 1035,
    @idMotivo = 3,
    @fechaInicio = '2023-10-01',
    @fechaFin = '2023-10-05',
    @comentarios = 'Vacaciones de verano';

SELECT numNomina, nombre, diasVacaciones
FROM usuarios
WHERE numNomina = 1035;