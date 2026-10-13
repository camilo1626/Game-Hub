BACKUP DATABASE GameHub
TO DISK = 'GameHub_respaldo.bak'
WITH INIT, NAME = 'Copia de GameHub antes de la actualización de seguridad';
GO

-- Comprueba que la copia se puede leer (tampoco cambia nada)
RESTORE VERIFYONLY FROM DISK = 'GameHub_respaldo.bak';
GO