from videojuegos.Juegos.aventura import JuegoAventura
from videojuegos.Juegos.competitivo import JuegoCompetitivo
from videojuegos.Juegos.terror import JuegoTerror
from videojuegos.Juegos.educativo import JuegoEducativo
from videojuegos.Juegos.shooter import JuegoDisparos

TIPOS = {
    "JuegoAventura": JuegoAventura,
    "JuegoCompetitivo": JuegoCompetitivo,
    "JuegoTerror": JuegoTerror,
    "JuegoEducativo": JuegoEducativo,
    "JuegoDisparos": JuegoDisparos,
}