import requests
from bs4 import BeautifulSoup
import yt_dlp
import re

def mostrar_formatos_disponibles(url):
    # Configuración para solo extraer información
    opciones_info = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(opciones_info) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            print("\nFormatos disponibles:")
            print("-------------------")
            for f in info['formats']:
                # Mostrar información relevante de cada formato
                formato = f['format_id']
                extension = f.get('ext', 'N/A')
                resolucion = f.get('resolution', 'N/A')
                
                # Manejo seguro del tamaño del archivo
                tamano = f.get('filesize')
                if tamano:
                    tamano = f"{tamano/1024/1024:.2f} MB"
                else:
                    tamano = 'N/A'
                
                print(f"ID: {formato} | Resolución: {resolucion} | Formato: {extension} | Tamaño: {tamano}")
            return True
        except Exception as e:
            print(f"Error al obtener formatos: {str(e)}")
            return False

def descargar_video():
    # URL del video que quieres descargar
    url = "https://www.3cat.cat/tv3/sx3/lu/video/6180127/"
    
    # Primero mostrar los formatos disponibles
    if mostrar_formatos_disponibles(url):
        # Pedir al usuario que elija un formato
        formato_elegido = input("\nIngresa el ID del formato que deseas descargar (o 'best' para la mejor calidad): ")
        
        # Opciones de configuración para yt-dlp
        opciones = {
            'format': formato_elegido,
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': False,
            'no_warnings': False,
        }

        try:
            # Crear el objeto descargador
            descargador = yt_dlp.YoutubeDL(opciones)
            
            # Descargar el video
            descargador.download([url])
            
            print("\n¡Video descargado exitosamente!")
            
        except Exception as e:
            print(f"\nError al descargar el video: {str(e)}")

def obtener_urls_videos():
    # Lista para almacenar todas las URLs de todas las temporadas
    todas_urls = []
    
    # Iterar por cada temporada (1-4)
    for temporada in range(1, 5):
        # URL base para cada temporada
        url = f"https://www.3cat.cat/tv3/sx3/numberblocks/videos/temporada-{temporada}"
        
        try:
            # Realizar la petición HTTP
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parsear el HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar todos los enlaces dentro de elementos con clase 'titol'
            links = soup.select('.titol a')
            
            # Lista para almacenar URLs de esta temporada
            urls_temporada = []
            
            for link in links:
                url = link.get('href')
                if url and 'video' in url:
                    # Añadir 'https:' al inicio si la URL empieza con '//'
                    if url.startswith('//'):
                        url = 'https:' + url
                    urls_temporada.append(url)
            
            print(f"\nTemporada {temporada}:")
            print(f"Se encontraron {len(urls_temporada)} videos:")
            for i, url in enumerate(urls_temporada, 1):
                print(f"{i}. {url}")
            
            todas_urls.extend(urls_temporada)
            
        except requests.RequestException as e:
            print(f"Error al obtener la temporada {temporada}: {str(e)}")
            continue
    
    print(f"\nTotal de videos encontrados: {len(todas_urls)}")
    return todas_urls

if __name__ == "__main__":
    urls = obtener_urls_videos()
