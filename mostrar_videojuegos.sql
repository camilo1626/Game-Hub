USE GameHub;

SELECT
    v.id_videojuego,
    v.nombre,
    g.nombre AS genero,
    p.nombre AS plataforma,
    v.anio_lanzamiento,
    v.precio,
    d.nombre AS desarrollador,
    t.nombre AS tipo
FROM Videojuegos v
INNER JOIN Generos g
    ON v.id_genero = g.id_genero
INNER JOIN Plataformas p
    ON v.id_plataforma = p.id_plataforma
INNER JOIN Desarrolladores d
    ON v.id_desarrollador = d.id_desarrollador
INNER JOIN TiposVideojuego t
    ON v.id_tipo = t.id_tipo;