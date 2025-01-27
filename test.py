import requests
from bs4 import BeautifulSoup
import yt_dlp
import re
import os

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
            return info['formats'] if 'formats' in info else None
        except Exception as e:
            print(f"Error al obtener formatos: {str(e)}")
            return None

def descargar_video(url, formato_elegido, temporada):
    # Crear directorio para la temporada si no existe
    carpeta = f"temporada_{temporada}"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Opciones de configuración para yt-dlp
    opciones = {
        'format': formato_elegido,
        'outtmpl': os.path.join(carpeta, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }

    try:
        descargador = yt_dlp.YoutubeDL(opciones)
        descargador.download([url])
        return True
    except Exception as e:
        print(f"\nError al descargar {url}: {str(e)}")
        return False

def obtener_urls_videos():
    todas_urls = {}  # Cambiado a diccionario para mantener la temporada
    
    for temporada in range(1, 5):
        url = f"https://www.3cat.cat/tv3/sx3/numberblocks/videos/temporada-{temporada}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.select('.titol a')
            
            urls_temporada = []
            for link in links:
                url = link.get('href')
                if url and 'video' in url:
                    if url.startswith('//'):
                        url = 'https:' + url
                    urls_temporada.append(url)
            
            print(f"\nTemporada {temporada}:")
            print(f"Se encontraron {len(urls_temporada)} videos:")
            for i, url in enumerate(urls_temporada, 1):
                print(f"{i}. {url}")
            
            todas_urls[temporada] = urls_temporada
            
        except requests.RequestException as e:
            print(f"Error al obtener la temporada {temporada}: {str(e)}")
            continue
    
    total_videos = sum(len(urls) for urls in todas_urls.values())
    print(f"\nTotal de videos encontrados: {total_videos}")
    return todas_urls

def descargar_todos_videos():
    # Obtener todas las URLs
    todas_urls = obtener_urls_videos()
    
    if not todas_urls:
        print("No se encontraron videos para descargar.")
        return
    
    # Obtener el primer video para mostrar formatos disponibles
    primer_url = todas_urls[1][0]  # Primera URL de la primera temporada
    formatos = mostrar_formatos_disponibles(primer_url)
    
    if not formatos:
        print("Error al obtener formatos disponibles.")
        return
    
    # Pedir al usuario que elija un formato
    formato_elegido = input("\nIngresa el ID del formato que deseas descargar (o 'best' para la mejor calidad): ")
    
    # Contador para seguimiento
    total_videos = sum(len(urls) for urls in todas_urls.values())
    videos_descargados = 0
    
    # Descargar videos por temporada
    for temporada, urls in todas_urls.items():
        print(f"\nDescargando temporada {temporada}...")
        
        for i, url in enumerate(urls, 1):
            videos_descargados += 1
            print(f"\nDescargando video {videos_descargados}/{total_videos}")
            print(f"URL: {url}")
            
            # Intentar descargar con el formato elegido
            if not descargar_video(url, formato_elegido, temporada):
                print(f"Intentando descargar con la mejor calidad disponible...")
                descargar_video(url, 'best', temporada)

if __name__ == "__main__":
    descargar_todos_videos()
