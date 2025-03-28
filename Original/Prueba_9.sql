USE [master]
GO
/****** Object:  Database [Prueba_9]    Script Date: 25/03/2025 05:30:29 p. m. ******/
CREATE DATABASE [Prueba_9]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'Prueba_9', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\Prueba_9.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'Prueba_9_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\Prueba_9_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO
ALTER DATABASE [Prueba_9] SET COMPATIBILITY_LEVEL = 150
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [Prueba_9].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [Prueba_9] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [Prueba_9] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [Prueba_9] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [Prueba_9] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [Prueba_9] SET ARITHABORT OFF 
GO
ALTER DATABASE [Prueba_9] SET AUTO_CLOSE ON 
GO
ALTER DATABASE [Prueba_9] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [Prueba_9] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [Prueba_9] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [Prueba_9] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [Prueba_9] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [Prueba_9] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [Prueba_9] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [Prueba_9] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [Prueba_9] SET  ENABLE_BROKER 
GO
ALTER DATABASE [Prueba_9] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [Prueba_9] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [Prueba_9] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [Prueba_9] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [Prueba_9] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [Prueba_9] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [Prueba_9] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [Prueba_9] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [Prueba_9] SET  MULTI_USER 
GO
ALTER DATABASE [Prueba_9] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [Prueba_9] SET DB_CHAINING OFF 
GO
ALTER DATABASE [Prueba_9] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [Prueba_9] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [Prueba_9] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [Prueba_9] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [Prueba_9] SET QUERY_STORE = OFF
GO
USE [Prueba_9]
GO
/****** Object:  Table [dbo].[credenciales]    Script Date: 25/03/2025 05:30:29 p. m. ******/
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
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[departamento_puesto]    Script Date: 25/03/2025 05:30:29 p. m. ******/
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
/****** Object:  Table [dbo].[departamentos]    Script Date: 25/03/2025 05:30:29 p. m. ******/
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
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[incidencias]    Script Date: 25/03/2025 05:30:29 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[incidencias](
	[idIncidencia] [int] IDENTITY(1,1) NOT NULL,
	[numNomina_solicitante] [int] NOT NULL,
	[nombre_solicitante] [nvarchar](100) NOT NULL,
	[apellido_paterno] [nvarchar](100) NOT NULL,
	[apellido_materno] [nvarchar](100) NOT NULL,
	[fecha_solicitud] [date] NOT NULL,
	[puesto] [nvarchar](100) NOT NULL,
	[departamento] [nvarchar](100) NOT NULL,
	[dias_vacaciones] [int] NOT NULL,
	[motivo] [nvarchar](100) NOT NULL,
	[fecha_inicio] [date] NOT NULL,
	[fecha_fin] [date] NOT NULL,
	[num_dias] [int] NOT NULL,
	[observaciones] [nvarchar](500) NULL,
	[estatus] [nvarchar](50) NOT NULL,
	[jefe_directo] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idIncidencia] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[jefes]    Script Date: 25/03/2025 05:30:29 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[jefes](
	[idJefe] [int] NOT NULL,
	[numNomina] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idJefe] ASC,
	[numNomina] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[motivos]    Script Date: 25/03/2025 05:30:29 p. m. ******/
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
/****** Object:  Table [dbo].[puestos]    Script Date: 25/03/2025 05:30:29 p. m. ******/
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
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[roles]    Script Date: 25/03/2025 05:30:29 p. m. ******/
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
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[usuario_rol]    Script Date: 25/03/2025 05:30:29 p. m. ******/
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
/****** Object:  Table [dbo].[usuarios]    Script Date: 25/03/2025 05:30:29 p. m. ******/
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
	[correo_electronico] [nvarchar](255) NULL,
	[jefe_directo] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[numNomina] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[vacaciones]    Script Date: 25/03/2025 05:30:29 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vacaciones](
	[idVacaciones] [int] IDENTITY(1,1) NOT NULL,
	[numNomina] [int] NOT NULL,
	[diasVacaciones] [int] NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[idVacaciones] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
SET IDENTITY_INSERT [dbo].[credenciales] ON 
GO
INSERT [dbo].[credenciales] ([idCredencial], [numNomina], [username], [password]) VALUES (1, 1035, N'alan.valenciano', N'12345')
GO
INSERT [dbo].[credenciales] ([idCredencial], [numNomina], [username], [password]) VALUES (2, 712, N'abraham.palafox', N'12345')
GO
INSERT [dbo].[credenciales] ([idCredencial], [numNomina], [username], [password]) VALUES (3, 1242, N'yarenci.avila', N'12345')
GO
INSERT [dbo].[credenciales] ([idCredencial], [numNomina], [username], [password]) VALUES (4, 265, N'alejandro.cuevas', N'12345')
GO
INSERT [dbo].[credenciales] ([idCredencial], [numNomina], [username], [password]) VALUES (1001, 538, N'marcelo.elosegui', N'12345')
GO
INSERT [dbo].[credenciales] ([idCredencial], [numNomina], [username], [password]) VALUES (1002, 1267, N'osiel.martinez', N'12345')
GO
SET IDENTITY_INSERT [dbo].[credenciales] OFF
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (1, 1)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (1, 2)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (1, 3)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (1, 6)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (1, 7)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (1, 8)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (1, 13)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (1, 16)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (1, 17)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (1, 18)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (2, 13)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (2, 16)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (2, 17)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (3, 4)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (3, 6)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (3, 8)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (3, 12)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (3, 13)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (3, 16)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (3, 17)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (4, 5)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (4, 6)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (4, 8)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (4, 13)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (4, 16)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (4, 17)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (5, 6)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (5, 8)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (5, 13)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (5, 16)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (5, 17)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (6, 6)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (6, 8)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (6, 13)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (6, 16)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (6, 17)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (6, 21)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (7, 3)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (7, 6)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (7, 8)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (7, 10)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (7, 13)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (7, 14)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (7, 16)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (7, 17)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (7, 22)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (8, 6)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (8, 8)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (8, 13)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (8, 16)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (8, 17)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (8, 18)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (9, 6)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (9, 8)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (9, 13)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (9, 15)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (9, 16)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (9, 17)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (9, 19)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (10, 6)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (10, 8)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (10, 9)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (10, 11)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (10, 13)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (10, 14)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (10, 16)
GO
INSERT [dbo].[departamento_puesto] ([idDepartamento], [idPuesto]) VALUES (10, 20)
GO
SET IDENTITY_INSERT [dbo].[departamentos] ON 
GO
INSERT [dbo].[departamentos] ([idDepartamento], [nombreDepartamento]) VALUES (1, N'Administración')
GO
INSERT [dbo].[departamentos] ([idDepartamento], [nombreDepartamento]) VALUES (2, N'Compras')
GO
INSERT [dbo].[departamentos] ([idDepartamento], [nombreDepartamento]) VALUES (10, N'Control de Calidad')
GO
INSERT [dbo].[departamentos] ([idDepartamento], [nombreDepartamento]) VALUES (6, N'Control de Producción')
GO
INSERT [dbo].[departamentos] ([idDepartamento], [nombreDepartamento]) VALUES (4, N'Finanzas')
GO
INSERT [dbo].[departamentos] ([idDepartamento], [nombreDepartamento]) VALUES (8, N'Mantenimiento')
GO
INSERT [dbo].[departamentos] ([idDepartamento], [nombreDepartamento]) VALUES (7, N'Producción')
GO
INSERT [dbo].[departamentos] ([idDepartamento], [nombreDepartamento]) VALUES (9, N'Seguridad e Higiene y Medio Ambiente')
GO
INSERT [dbo].[departamentos] ([idDepartamento], [nombreDepartamento]) VALUES (5, N'Sistemas')
GO
INSERT [dbo].[departamentos] ([idDepartamento], [nombreDepartamento]) VALUES (3, N'Ventas')
GO
SET IDENTITY_INSERT [dbo].[departamentos] OFF
GO
SET IDENTITY_INSERT [dbo].[incidencias] ON 
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (1, 1035, N'Alan de Jesús', N'Valenciano', N'Llamas', CAST(N'2025-03-19' AS Date), N'Auxiliar', N'Sistemas', 7, N'vacaciones', CAST(N'2025-03-19' AS Date), CAST(N'2025-03-19' AS Date), 1, N'12345', N'Rechazada', 712)
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (2, 1035, N'Alan de Jesús', N'Valenciano', N'Llamas', CAST(N'2025-03-19' AS Date), N'Auxiliar', N'Sistemas', 7, N'sin_goce_sueldo', CAST(N'2025-03-19' AS Date), CAST(N'2025-03-19' AS Date), 1, N'123456', N'Aprobada', 712)
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (3, 1035, N'Alan de Jesús', N'Valenciano', N'Llamas', CAST(N'2025-03-19' AS Date), N'Auxiliar', N'Sistemas', 7, N'vacaciones', CAST(N'2025-03-20' AS Date), CAST(N'2025-03-20' AS Date), 1, N'123456', N'Aprobada', 712)
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (4, 1035, N'Alan de Jesús', N'Valenciano', N'Llamas', CAST(N'2025-03-21' AS Date), N'Auxiliar', N'Sistemas', 7, N'vacaciones', CAST(N'2025-03-24' AS Date), CAST(N'2025-03-27' AS Date), 4, N'prueba 1', N'Aprobada', 712)
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (5, 1242, N'Yarenci', N'Avila', N'Murillo', CAST(N'2025-03-21' AS Date), N'Lider', N'Administración', 7, N'vacaciones', CAST(N'2025-03-24' AS Date), CAST(N'2025-03-27' AS Date), 4, N'Prueba 1 desde rol usuario', N'Rechazada', 1267)
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (6, 1242, N'Yarenci', N'Avila', N'Murillo', CAST(N'2025-03-21' AS Date), N'Lider', N'Administración', 7, N'sin_goce_sueldo', CAST(N'2025-03-24' AS Date), CAST(N'2025-03-27' AS Date), 4, N'Prueba 2', N'Aprobada', 1267)
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (7, 1035, N'Alan de Jesús', N'Valenciano', N'Llamas', CAST(N'2025-03-21' AS Date), N'Auxiliar', N'Sistemas', 7, N'vacaciones', CAST(N'2025-03-24' AS Date), CAST(N'2025-03-27' AS Date), 4, N'PRUEBA 1', N'Pendiente', 538)
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (8, 1242, N'Yarenci', N'Avila', N'Murillo', CAST(N'2025-03-25' AS Date), N'Lider', N'Administración', 7, N'goce_sueldo', CAST(N'2025-03-26' AS Date), CAST(N'2025-03-28' AS Date), 3, N'Prueba 12345', N'Rechazada', 1267)
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (9, 1035, N'Alan de Jesús', N'Valenciano', N'Llamas', CAST(N'2025-03-25' AS Date), N'Auxiliar', N'Sistemas', 7, N'sin_goce_sueldo', CAST(N'2025-04-02' AS Date), CAST(N'2025-04-05' AS Date), 4, N'12345', N'Pendiente', 538)
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (10, 1035, N'Alan de Jesús', N'Valenciano', N'Llamas', CAST(N'2025-03-25' AS Date), N'Auxiliar', N'Sistemas', 7, N'olvido_gafete', CAST(N'2025-03-26' AS Date), CAST(N'2025-03-27' AS Date), 2, N'Prueba 12345', N'Pendiente', 538)
GO
INSERT [dbo].[incidencias] ([idIncidencia], [numNomina_solicitante], [nombre_solicitante], [apellido_paterno], [apellido_materno], [fecha_solicitud], [puesto], [departamento], [dias_vacaciones], [motivo], [fecha_inicio], [fecha_fin], [num_dias], [observaciones], [estatus], [jefe_directo]) VALUES (11, 1035, N'Alan de Jesús', N'Valenciano', N'Llamas', CAST(N'2025-03-25' AS Date), N'Auxiliar', N'Sistemas', 7, N'vacaciones', CAST(N'2025-03-26' AS Date), CAST(N'2025-03-27' AS Date), 2, N'12345', N'Pendiente', 538)
GO
SET IDENTITY_INSERT [dbo].[incidencias] OFF
GO
SET IDENTITY_INSERT [dbo].[motivos] ON 
GO
INSERT [dbo].[motivos] ([idMotivo], [nombreMotivo]) VALUES (1, N'Permiso sin goce de sueldo')
GO
INSERT [dbo].[motivos] ([idMotivo], [nombreMotivo]) VALUES (2, N'Permiso con goce de sueldo')
GO
INSERT [dbo].[motivos] ([idMotivo], [nombreMotivo]) VALUES (3, N'Vacaciones')
GO
INSERT [dbo].[motivos] ([idMotivo], [nombreMotivo]) VALUES (4, N'Olvido de gafete')
GO
INSERT [dbo].[motivos] ([idMotivo], [nombreMotivo]) VALUES (5, N'Tiempo x Tiempo')
GO
SET IDENTITY_INSERT [dbo].[motivos] OFF
GO
SET IDENTITY_INSERT [dbo].[puestos] ON 
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (21, N'Almacenista')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (8, N'Asistente de Gerente')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (7, N'Asistente para el Gerente General de Administración')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (17, N'Auxiliar')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (1, N'Director General')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (19, N'Enfermero(a)')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (6, N'Gerente')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (3, N'Gerente de Planta')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (2, N'Gerente General de Administración')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (4, N'Gerente General de Ventas')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (5, N'Gerente Senior de Finanzas')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (20, N'Inspector')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (16, N'Lider')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (15, N'Medico')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (22, N'Operario')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (13, N'Supervisor')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (12, N'Supervisor de Atención a Cliente')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (11, N'Supervisor ISO')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (9, N'Supervisor Senior de APQP')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (10, N'Supervisor Senior de Producción')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (18, N'Tecnico')
GO
INSERT [dbo].[puestos] ([idPuesto], [nombrePuesto]) VALUES (14, N'Traductor')
GO
SET IDENTITY_INSERT [dbo].[puestos] OFF
GO
SET IDENTITY_INSERT [dbo].[roles] ON 
GO
INSERT [dbo].[roles] ([idRol], [nombreRol]) VALUES (1, N'Admin')
GO
INSERT [dbo].[roles] ([idRol], [nombreRol]) VALUES (3, N'Gerente')
GO
INSERT [dbo].[roles] ([idRol], [nombreRol]) VALUES (4, N'Supervisor')
GO
INSERT [dbo].[roles] ([idRol], [nombreRol]) VALUES (2, N'Usuario')
GO
SET IDENTITY_INSERT [dbo].[roles] OFF
GO
INSERT [dbo].[usuario_rol] ([numNomina], [idRol]) VALUES (265, 4)
GO
INSERT [dbo].[usuario_rol] ([numNomina], [idRol]) VALUES (538, 3)
GO
INSERT [dbo].[usuario_rol] ([numNomina], [idRol]) VALUES (712, 3)
GO
INSERT [dbo].[usuario_rol] ([numNomina], [idRol]) VALUES (1035, 1)
GO
INSERT [dbo].[usuario_rol] ([numNomina], [idRol]) VALUES (1242, 2)
GO
INSERT [dbo].[usuario_rol] ([numNomina], [idRol]) VALUES (1267, 4)
GO
INSERT [dbo].[usuarios] ([numNomina], [nombre], [apellidoPaterno], [apellidoMaterno], [idDepartamento], [idPuesto], [diasVacaciones], [correo_electronico], [jefe_directo]) VALUES (265, N'Cesar Alejandro', N'Cuevas', N'López', 5, 8, 7, N'soporte@tohken.mx', 538)
GO
INSERT [dbo].[usuarios] ([numNomina], [nombre], [apellidoPaterno], [apellidoMaterno], [idDepartamento], [idPuesto], [diasVacaciones], [correo_electronico], [jefe_directo]) VALUES (538, N'Marcelo', N'Elosegui', N'Rico', 1, 6, 14, N'soporte@tohken.mx', NULL)
GO
INSERT [dbo].[usuarios] ([numNomina], [nombre], [apellidoPaterno], [apellidoMaterno], [idDepartamento], [idPuesto], [diasVacaciones], [correo_electronico], [jefe_directo]) VALUES (712, N'Jesús Abraham', N'Palafox', N'Romo', 5, 16, 7, N'soporte@tohken.mx', 538)
GO
INSERT [dbo].[usuarios] ([numNomina], [nombre], [apellidoPaterno], [apellidoMaterno], [idDepartamento], [idPuesto], [diasVacaciones], [correo_electronico], [jefe_directo]) VALUES (1035, N'Alan de Jesús', N'Valenciano', N'Llamas', 5, 17, 7, N'soporte@tohken.mx', 538)
GO
INSERT [dbo].[usuarios] ([numNomina], [nombre], [apellidoPaterno], [apellidoMaterno], [idDepartamento], [idPuesto], [diasVacaciones], [correo_electronico], [jefe_directo]) VALUES (1242, N'Yarenci', N'Avila', N'Murillo', 1, 16, 7, N'soporte@tohken.mx', 1267)
GO
INSERT [dbo].[usuarios] ([numNomina], [nombre], [apellidoPaterno], [apellidoMaterno], [idDepartamento], [idPuesto], [diasVacaciones], [correo_electronico], [jefe_directo]) VALUES (1267, N'Osiel', N'Martinez', N'Arias', 1, 13, 12, N'soporte@tohken.mx', 538)
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__credenci__F3DBC5721C204553]    Script Date: 25/03/2025 05:30:29 p. m. ******/
ALTER TABLE [dbo].[credenciales] ADD UNIQUE NONCLUSTERED 
(
	[username] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__departam__97ABAFF591518337]    Script Date: 25/03/2025 05:30:29 p. m. ******/
ALTER TABLE [dbo].[departamentos] ADD UNIQUE NONCLUSTERED 
(
	[nombreDepartamento] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__puestos__0CBEA40B136DD121]    Script Date: 25/03/2025 05:30:29 p. m. ******/
ALTER TABLE [dbo].[puestos] ADD UNIQUE NONCLUSTERED 
(
	[nombrePuesto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [uq_nombrePuesto]    Script Date: 25/03/2025 05:30:29 p. m. ******/
ALTER TABLE [dbo].[puestos] ADD  CONSTRAINT [uq_nombrePuesto] UNIQUE NONCLUSTERED 
(
	[nombrePuesto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__roles__2787B00C2DF6F9D8]    Script Date: 25/03/2025 05:30:29 p. m. ******/
ALTER TABLE [dbo].[roles] ADD UNIQUE NONCLUSTERED 
(
	[nombreRol] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
GO
ALTER TABLE [dbo].[incidencias] ADD  DEFAULT ('Pendiente') FOR [estatus]
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
ALTER TABLE [dbo].[incidencias]  WITH CHECK ADD FOREIGN KEY([jefe_directo])
REFERENCES [dbo].[usuarios] ([numNomina])
GO
ALTER TABLE [dbo].[incidencias]  WITH CHECK ADD FOREIGN KEY([numNomina_solicitante])
REFERENCES [dbo].[usuarios] ([numNomina])
GO
ALTER TABLE [dbo].[jefes]  WITH CHECK ADD FOREIGN KEY([idJefe])
REFERENCES [dbo].[usuarios] ([numNomina])
GO
ALTER TABLE [dbo].[jefes]  WITH CHECK ADD FOREIGN KEY([numNomina])
REFERENCES [dbo].[usuarios] ([numNomina])
GO
ALTER TABLE [dbo].[usuario_rol]  WITH CHECK ADD FOREIGN KEY([idRol])
REFERENCES [dbo].[roles] ([idRol])
GO
ALTER TABLE [dbo].[usuario_rol]  WITH CHECK ADD FOREIGN KEY([numNomina])
REFERENCES [dbo].[usuarios] ([numNomina])
GO
ALTER TABLE [dbo].[usuarios]  WITH CHECK ADD  CONSTRAINT [fk_jefe_directo] FOREIGN KEY([jefe_directo])
REFERENCES [dbo].[usuarios] ([numNomina])
GO
ALTER TABLE [dbo].[usuarios] CHECK CONSTRAINT [fk_jefe_directo]
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
ALTER TABLE [dbo].[vacaciones]  WITH CHECK ADD FOREIGN KEY([numNomina])
REFERENCES [dbo].[usuarios] ([numNomina])
GO
USE [master]
GO
ALTER DATABASE [Prueba_9] SET  READ_WRITE 
GO
