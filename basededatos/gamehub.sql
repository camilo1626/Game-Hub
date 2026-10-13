IF DB_ID('GameHub') IS NULL
    CREATE DATABASE GameHub;
GO

USE GameHub;
GO


IF OBJECT_ID('Generos', 'U') IS NULL
    CREATE TABLE Generos (
        id_genero INT IDENTITY(1,1) PRIMARY KEY,
        nombre    NVARCHAR(50) NOT NULL
    );

IF OBJECT_ID('Plataformas', 'U') IS NULL
    CREATE TABLE Plataformas (
        id_plataforma INT IDENTITY(1,1) PRIMARY KEY,
        nombre        NVARCHAR(50) NOT NULL
    );

IF OBJECT_ID('Desarrolladores', 'U') IS NULL
    CREATE TABLE Desarrolladores (
        id_desarrollador INT IDENTITY(1,1) PRIMARY KEY,
        nombre           NVARCHAR(100) NOT NULL
    );

IF OBJECT_ID('TiposVideojuego', 'U') IS NULL
    CREATE TABLE TiposVideojuego (
        id_tipo INT IDENTITY(1,1) PRIMARY KEY,
        nombre  NVARCHAR(50) NOT NULL
    );
GO

-- ---------- Tablas principales ----------

-- rol puede ser 'usuario' o 'admin'
-- contrasena guarda el HASH (no la contraseña escrita), por eso necesita 255 caracteres
IF OBJECT_ID('Usuarios', 'U') IS NULL
    CREATE TABLE Usuarios (
        id_usuario INT IDENTITY(1,1) PRIMARY KEY,
        nombre     NVARCHAR(100) NOT NULL,
        correo     NVARCHAR(100) NOT NULL UNIQUE,
        telefono   NVARCHAR(20),
        contrasena NVARCHAR(255) NOT NULL,
        rol        NVARCHAR(20) NOT NULL DEFAULT 'usuario'
    );
GO

-- disponible = 1 se ve en el catálogo, disponible = 0 está reservado (ya se aceptó un pedido)
IF OBJECT_ID('Videojuegos', 'U') IS NULL
    CREATE TABLE Videojuegos (
        id_videojuego    INT IDENTITY(1,1) PRIMARY KEY,
        nombre           NVARCHAR(100) NOT NULL,
        id_genero        INT NOT NULL REFERENCES Generos(id_genero),
        id_plataforma    INT NOT NULL REFERENCES Plataformas(id_plataforma),
        año_lanzamiento  INT NOT NULL,
        precio           DECIMAL(10,2) NOT NULL DEFAULT 0,
        id_desarrollador INT NOT NULL REFERENCES Desarrolladores(id_desarrollador),
        id_tipo          INT NOT NULL REFERENCES TiposVideojuego(id_tipo),
        estado           NVARCHAR(20) NOT NULL DEFAULT 'Bueno',
        tipo_oferta      NVARCHAR(20) NOT NULL DEFAULT 'Venta',
        id_usuario       INT NOT NULL REFERENCES Usuarios(id_usuario),
        disponible       BIT NOT NULL DEFAULT 1,
        imagen           NVARCHAR(500) NULL
    );
GO

-- estado puede ser 'Pendiente', 'Aceptada' o 'Rechazada'
IF OBJECT_ID('Solicitudes', 'U') IS NULL
    CREATE TABLE Solicitudes (
        id_solicitud   INT IDENTITY(1,1) PRIMARY KEY,
        id_videojuego  INT NOT NULL REFERENCES Videojuegos(id_videojuego),
        id_solicitante INT NOT NULL REFERENCES Usuarios(id_usuario),
        mensaje        NVARCHAR(200),
        estado         NVARCHAR(20) NOT NULL DEFAULT 'Pendiente'
    );

IF OBJECT_ID('Notificaciones', 'U') IS NULL
    CREATE TABLE Notificaciones (
        id_notificacion INT IDENTITY(1,1) PRIMARY KEY,
        id_usuario      INT NOT NULL REFERENCES Usuarios(id_usuario),
        mensaje         NVARCHAR(300) NOT NULL,
        leida           BIT NOT NULL DEFAULT 0
    );
GO

GO

-- ---------- Columnas nuevas en tablas viejas (solo si faltan) ----------

IF COL_LENGTH('Usuarios', 'telefono') IS NULL
    ALTER TABLE Usuarios ADD telefono NVARCHAR(20) NULL;

IF COL_LENGTH('Usuarios', 'rol') IS NULL
    ALTER TABLE Usuarios ADD rol NVARCHAR(20) NOT NULL DEFAULT 'usuario';

-- Agranda la columna de la contraseña para que quepa el hash (no borra nada)
IF COL_LENGTH('Usuarios', 'contrasena') < 510
    ALTER TABLE Usuarios ALTER COLUMN contrasena NVARCHAR(255) NOT NULL;

IF COL_LENGTH('Videojuegos', 'disponible') IS NULL
    ALTER TABLE Videojuegos ADD disponible BIT NOT NULL DEFAULT 1;

IF COL_LENGTH('Videojuegos', 'imagen') IS NULL
    ALTER TABLE Videojuegos ADD imagen NVARCHAR(500) NULL;

IF COL_LENGTH('Notificaciones', 'leida') IS NULL
    ALTER TABLE Notificaciones ADD leida BIT NOT NULL DEFAULT 0;
GO

-- Versiones viejas llamaban "juego_ofrecido" a la columna "mensaje"
IF COL_LENGTH('Solicitudes', 'mensaje') IS NULL AND COL_LENGTH('Solicitudes', 'juego_ofrecido') IS NOT NULL
    EXEC sp_rename 'Solicitudes.juego_ofrecido', 'mensaje', 'COLUMN';
GO

IF COL_LENGTH('Solicitudes', 'mensaje') IS NULL
    ALTER TABLE Solicitudes ADD mensaje NVARCHAR(200) NULL;
GO

-- ---------- Opciones de las listas (solo si las tablas están vacías) ----------

IF NOT EXISTS (SELECT 1 FROM Generos)
    INSERT INTO Generos (nombre) VALUES
        ('Acción'), ('Aventura'), ('Deportes'), ('Terror'), ('Estrategia'), ('Educativo'), ('Carreras');

IF NOT EXISTS (SELECT 1 FROM Plataformas)
    INSERT INTO Plataformas (nombre) VALUES
        ('PC'), ('PlayStation 4'), ('PlayStation 5'), ('Xbox One'), ('Xbox Series'), ('Nintendo Switch');

IF NOT EXISTS (SELECT 1 FROM Desarrolladores)
    INSERT INTO Desarrolladores (nombre) VALUES
        ('Nintendo'), ('Capcom'), ('Mojang'), ('EA Sports'), ('Ubisoft'), ('Rockstar Games'), ('Otro');

IF NOT EXISTS (SELECT 1 FROM TiposVideojuego)
    INSERT INTO TiposVideojuego (nombre) VALUES
        ('JuegoAventura'), ('JuegoCompetitivo'), ('JuegoTerror'), ('JuegoEducativo'), ('JuegoDisparos');
GO

-- ---------- Índice para aceptar solicitudes sin bloquear toda la tabla ----------
-- Con este índice SQL Server va directo a las solicitudes de UN juego (no revisa toda la tabla),
-- y así dos personas que aceptan pedidos de juegos distintos no se estorban.
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'IX_Solicitudes_Videojuego' AND object_id = OBJECT_ID('Solicitudes'))
    CREATE INDEX IX_Solicitudes_Videojuego ON Solicitudes (id_videojuego, estado);
GO
