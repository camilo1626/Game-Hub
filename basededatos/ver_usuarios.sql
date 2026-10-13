USE GameHub;
SELECT id_usuario AS ID,
       nombre     AS Nombre,
       correo     AS Correo,
       telefono   AS Telefono,
       rol        AS Rol,
       CASE WHEN contrasena LIKE 'scrypt:%' OR contrasena LIKE 'pbkdf2:%'
            THEN 'Protegida (hash)' ELSE 'SIN hash (migrar)' END AS Contrasena
FROM Usuarios
ORDER BY id_usuario;

-- 2. Buscar a UNA persona por su correo (cambia el correo)
SELECT nombre, correo, telefono, rol
FROM Usuarios
WHERE correo = 'juan@gamehub.com';
