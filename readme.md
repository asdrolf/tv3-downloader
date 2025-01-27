# Descarregador de Vídeos 3CAT

Script per descarregar sèries completes de la plataforma 3CAT (TV3). Actualment configurat per descarregar Numberblocks, però es pot modificar per a qualsevol sèrie disponible a la plataforma.

## Configuració

Per descarregar una sèrie diferent, modifica aquestes variables a `test.py`:

# A la funció obtener_urls_videos():
url = f"https://www.3cat.cat/tv3/sx3/numberblocks/videos/temporada-{temporada}"

Canvia:
- `numberblocks` pel nom de la sèrie que vulguis descarregar
- `range(1, 5)` pel rang de temporades disponibles

## Requeriments

pip install requests beautifulsoup4 yt-dlp

## Ús

1. Executar l'script:
python test.py

2. Seleccionar la qualitat de vídeo quan es mostri la llista de formats disponibles

L'script crearà automàticament carpetes per temporada i descarregarà tots els episodis.

## Estructura

temporada_1/
    episodi1.mp4
    episodi2.mp4
temporada_2/
    episodi1.mp4
    ...

## Nota

Assegura't de tenir els permisos necessaris per descarregar el contingut.

-------------------------------------------

# Descargador de Videos 3CAT

Script para descargar series completas de la plataforma 3CAT (TV3). Actualmente configurado para descargar Numberblocks, pero puede modificarse para cualquier serie disponible en la plataforma.

## Configuración

Para descargar una serie diferente, modifica estas variables en `test.py`:

# En la función obtener_urls_videos():
url = f"https://www.3cat.cat/tv3/sx3/numberblocks/videos/temporada-{temporada}"

Cambia:
- `numberblocks` por el nombre de la serie que quieras descargar
- `range(1, 5)` por el rango de temporadas disponibles

## Requisitos

pip install requests beautifulsoup4 yt-dlp

## Uso

1. Ejecutar el script:
python test.py

2. Seleccionar la calidad de video cuando se muestre la lista de formatos disponibles

El script creará automáticamente carpetas por temporada y descargará todos los episodios.

## Estructura

temporada_1/
    episodio1.mp4
    episodio2.mp4
temporada_2/
    episodio1.mp4
    ...

## Nota

Asegúrate de tener los permisos necesarios para descargar el contenido.