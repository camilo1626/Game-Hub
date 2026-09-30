USE GameHub;
GO

ALTER TABLE Usuarios ADD contrasena NVARCHAR(50) NULL;
GO

UPDATE Usuarios SET contrasena = '1234' WHERE contrasena IS NULL;
GO

SELECT id_usuario, nombre, correo, contrasena FROM Usuarios;
