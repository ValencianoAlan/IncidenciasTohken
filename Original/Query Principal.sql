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

-- Tabla para relacionar usuarios con departamentos
CREATE TABLE usuario_departamento (
    numNomina INT NOT NULL,
    idDepartamento INT NOT NULL,
    PRIMARY KEY (numNomina, idDepartamento),
    FOREIGN KEY (numNomina) REFERENCES usuarios(numNomina),
    FOREIGN KEY (idDepartamento) REFERENCES departamentos(idDepartamento)
);

CREATE TABLE vacaciones (
    numNomina INT PRIMARY KEY,  -- Relación directa con el usuario
    diasVacaciones INT NOT NULL,  -- Días de vacaciones restantes
    FOREIGN KEY (numNomina) REFERENCES usuarios(numNomina)
);

select * from credenciales;
select * from roles;
select * from usuario_rol;
select * from usuarios;
select * from puestos;
select * from usuario_puesto;
select * from departamentos ORDER BY idDepartamento;

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
('Gerente'),
('Asistente de Gerente'),
('Supervisor'),
('Lider'),
('Auxiliar');