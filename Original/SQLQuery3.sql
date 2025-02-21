Use Prueba_4

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

select * from credenciales;
select * from roles;
select * from usuario_rol;
select * from usuarios;

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