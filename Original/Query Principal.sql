Use Prueba_5

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