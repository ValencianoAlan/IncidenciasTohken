USE Prueba_7
GO
/****** Object:  Database [Prueba_6]    Script Date: 05/03/2025 02:38:36 p. m. ******/
CREATE DATABASE [Prueba_7]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'Prueba_5', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\Prueba_5_1508484335.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'Prueba_5_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\Prueba_5_log_1782233627.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [Prueba_6] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [Prueba_6].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [Prueba_6] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [Prueba_6] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [Prueba_6] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [Prueba_6] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [Prueba_6] SET ARITHABORT OFF 
GO
ALTER DATABASE [Prueba_6] SET AUTO_CLOSE ON 
GO
ALTER DATABASE [Prueba_6] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [Prueba_6] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [Prueba_6] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [Prueba_6] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [Prueba_6] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [Prueba_6] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [Prueba_6] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [Prueba_6] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [Prueba_6] SET  ENABLE_BROKER 
GO
ALTER DATABASE [Prueba_6] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [Prueba_6] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [Prueba_6] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [Prueba_6] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [Prueba_6] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [Prueba_6] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [Prueba_6] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [Prueba_6] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [Prueba_6] SET  MULTI_USER 
GO
ALTER DATABASE [Prueba_6] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [Prueba_6] SET DB_CHAINING OFF 
GO
ALTER DATABASE [Prueba_6] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [Prueba_6] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [Prueba_6] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [Prueba_6] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [Prueba_6] SET QUERY_STORE = OFF
GO
USE [Prueba_6]
GO
/****** Object:  Table [dbo].[credenciales]    Script Date: 05/03/2025 02:38:36 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[credenciales](
	[idCredencial] [int] IDENTITY(1,1) NOT NULL,
	[numNomina] [int] NOT NULL,
	[username] [nvarchar](50) NOT NULL,
	[password] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idCredencial] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[departamento_puesto]    Script Date: 05/03/2025 02:38:37 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[departamento_puesto](
	[idDepartamento] [int] NOT NULL,
	[idPuesto] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idDepartamento] ASC,
	[idPuesto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[departamentos]    Script Date: 05/03/2025 02:38:37 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[departamentos](
	[idDepartamento] [int] IDENTITY(1,1) NOT NULL,
	[nombreDepartamento] [nvarchar](100) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idDepartamento] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[nombreDepartamento] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[incidencias]    Script Date: 05/03/2025 02:38:37 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[incidencias](
	[idIncidencia] [int] IDENTITY(1,1) NOT NULL,
	[numNomina] [int] NOT NULL,
	[idMotivo] [int] NOT NULL,
	[fechaSolicitud] [date] NOT NULL,
	[fechaInicio] [date] NOT NULL,
	[fechaFin] [date] NOT NULL,
	[numDias] [int] NULL,
	[comentarios] [nvarchar](500) NULL,
PRIMARY KEY CLUSTERED 
(
	[idIncidencia] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[motivos]    Script Date: 05/03/2025 02:38:37 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[motivos](
	[idMotivo] [int] IDENTITY(1,1) NOT NULL,
	[nombreMotivo] [nvarchar](100) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idMotivo] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[puestos]    Script Date: 05/03/2025 02:38:37 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[puestos](
	[idPuesto] [int] IDENTITY(1,1) NOT NULL,
	[nombrePuesto] [nvarchar](100) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idPuesto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[nombrePuesto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
 CONSTRAINT [uq_nombrePuesto] UNIQUE NONCLUSTERED 
(
	[nombrePuesto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[roles]    Script Date: 05/03/2025 02:38:37 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[roles](
	[idRol] [int] IDENTITY(1,1) NOT NULL,
	[nombreRol] [nvarchar](50) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idRol] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
	[nombreRol] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[usuario_rol]    Script Date: 05/03/2025 02:38:37 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[usuario_rol](
	[numNomina] [int] NOT NULL,
	[idRol] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[numNomina] ASC,
	[idRol] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[usuarios]    Script Date: 05/03/2025 02:38:37 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[usuarios](
	[numNomina] [int] NOT NULL,
	[nombre] [nvarchar](100) NOT NULL,
	[apellidoPaterno] [nvarchar](100) NULL,
	[apellidoMaterno] [nvarchar](100) NULL,
	[idDepartamento] [int] NULL,
	[idPuesto] [int] NULL,
	[diasVacaciones] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[numNomina] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[incidencias] ADD  DEFAULT (getdate()) FOR [fechaSolicitud]
GO
ALTER TABLE [dbo].[usuarios] ADD  DEFAULT ((0)) FOR [diasVacaciones]
GO
ALTER TABLE [dbo].[credenciales]  WITH CHECK ADD FOREIGN KEY([numNomina])
REFERENCES [dbo].[usuarios] ([numNomina])
GO
ALTER TABLE [dbo].[departamento_puesto]  WITH CHECK ADD FOREIGN KEY([idDepartamento])
REFERENCES [dbo].[departamentos] ([idDepartamento])
GO
ALTER TABLE [dbo].[departamento_puesto]  WITH CHECK ADD FOREIGN KEY([idPuesto])
REFERENCES [dbo].[puestos] ([idPuesto])
GO
ALTER TABLE [dbo].[departamento_puesto]  WITH CHECK ADD  CONSTRAINT [fk_departamento] FOREIGN KEY([idDepartamento])
REFERENCES [dbo].[departamentos] ([idDepartamento])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[departamento_puesto] CHECK CONSTRAINT [fk_departamento]
GO
ALTER TABLE [dbo].[departamento_puesto]  WITH CHECK ADD  CONSTRAINT [fk_puesto] FOREIGN KEY([idPuesto])
REFERENCES [dbo].[puestos] ([idPuesto])
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[departamento_puesto] CHECK CONSTRAINT [fk_puesto]
GO
ALTER TABLE [dbo].[incidencias]  WITH CHECK ADD FOREIGN KEY([idMotivo])
REFERENCES [dbo].[motivos] ([idMotivo])
GO
ALTER TABLE [dbo].[incidencias]  WITH CHECK ADD FOREIGN KEY([numNomina])
REFERENCES [dbo].[usuarios] ([numNomina])
GO
ALTER TABLE [dbo].[usuario_rol]  WITH CHECK ADD FOREIGN KEY([idRol])
REFERENCES [dbo].[roles] ([idRol])
GO
ALTER TABLE [dbo].[usuario_rol]  WITH CHECK ADD FOREIGN KEY([numNomina])
REFERENCES [dbo].[usuarios] ([numNomina])
GO
ALTER TABLE [dbo].[usuarios]  WITH CHECK ADD  CONSTRAINT [fk_usuario_departamento] FOREIGN KEY([idDepartamento])
REFERENCES [dbo].[departamentos] ([idDepartamento])
GO
ALTER TABLE [dbo].[usuarios] CHECK CONSTRAINT [fk_usuario_departamento]
GO
ALTER TABLE [dbo].[usuarios]  WITH CHECK ADD  CONSTRAINT [fk_usuario_puesto] FOREIGN KEY([idPuesto])
REFERENCES [dbo].[puestos] ([idPuesto])
GO
ALTER TABLE [dbo].[usuarios] CHECK CONSTRAINT [fk_usuario_puesto]
GO
/****** Object:  StoredProcedure [dbo].[crear_incidencia]    Script Date: 05/03/2025 02:38:37 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[crear_incidencia]
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
GO
USE [master]
GO
ALTER DATABASE [Prueba_6] SET  READ_WRITE 
GO
