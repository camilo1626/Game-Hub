USE GameHub;
GO

DROP TABLE IF EXISTS Solicitudes, Solicitud, Videojuegos, videojuego,
                     Usuarios, Usuario, TiposVideojuego, Desarrolladores, Plataformas, Generos;
GO

CREATE TABLE Generos (
    id_genero INT IDENTITY(1,1) PRIMARY KEY,
    nombre    NVARCHAR(50) NOT NULL
);

CREATE TABLE Plataformas (
    id_plataforma INT IDENTITY(1,1) PRIMARY KEY,
    nombre        NVARCHAR(50) NOT NULL
);

CREATE TABLE Desarrolladores (
    id_desarrollador INT IDENTITY(1,1) PRIMARY KEY,
    nombre           NVARCHAR(100) NOT NULL
);

CREATE TABLE TiposVideojuego (
    id_tipo INT IDENTITY(1,1) PRIMARY KEY,
    nombre  NVARCHAR(50) NOT NULL
);

CREATE TABLE Usuarios (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    nombre     NVARCHAR(100) NOT NULL,
    telefono   NVARCHAR(20),
    correo     NVARCHAR(100)
);

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
    id_usuario       INT NULL REFERENCES Usuarios(id_usuario),
    disponible       BIT NOT NULL DEFAULT 1
);

CREATE TABLE Solicitudes (
    id_solicitud   INT IDENTITY(1,1) PRIMARY KEY,
    id_videojuego  INT NOT NULL REFERENCES Videojuegos(id_videojuego),
    id_solicitante INT NOT NULL REFERENCES Usuarios(id_usuario),
    juego_ofrecido NVARCHAR(100),
    estado         NVARCHAR(20) NOT NULL DEFAULT 'Pendiente',
    fecha          DATETIME NOT NULL DEFAULT GETDATE()
);
GO

INSERT INTO Generos (nombre) VALUES
    ('Acción'), ('Aventura'), ('Deportes'), ('Terror'), ('Estrategia'), ('Educativo'), ('Carreras');

INSERT INTO Plataformas (nombre) VALUES
    ('PC'), ('PlayStation 4'), ('PlayStation 5'), ('Xbox One'), ('Xbox Series'), ('Nintendo Switch');

INSERT INTO Desarrolladores (nombre) VALUES
    ('Nintendo'), ('Capcom'), ('Mojang'), ('EA Sports'), ('Ubisoft'), ('Rockstar Games'), ('Otro');

INSERT INTO TiposVideojuego (nombre) VALUES
    ('JuegoAventura'), ('JuegoCompetitivo'), ('JuegoTerror'), ('JuegoEducativo'), ('JuegoDisparos');

INSERT INTO Usuarios (nombre, telefono, correo) VALUES
    ('Juan Garcia', '3192695345', 'juan@gamehub.com'),
    ('Camilo Cortes', '3180895981', 'camilo@gamehub.com');

INSERT INTO Videojuegos (nombre, id_genero, id_plataforma, año_lanzamiento, precio, id_desarrollador, id_tipo, estado, tipo_oferta, id_usuario) VALUES
    ('GTA V', 1, 2, 2013, 80000, 6, 1, 'Bueno', 'Venta', 1),
    ('FIFA 23', 3, 2, 2022, 0, 4, 2, 'Nuevo', 'Intercambio', 1),
    ('Minecraft', 2, 1, 2011, 40000, 3, 1, 'Bueno', 'Venta', 2),
    ('Resident Evil 4', 4, 2, 2005, 60000, 2, 3, 'Bueno', 'Venta', 2),
    ('Mario Kart 8', 7, 6, 2017, 0, 1, 2, 'Nuevo', 'Intercambio', 2),
    ('Age of Empires', 5, 1, 1997, 0, 7, 4, 'Regular', 'Donación', 2);
GO

SELECT name FROM GameHub.sys.tables;
