import logging
import os
import requests
import pyodbc  # Para conectar con SQL Server
from datetime import datetime, timedelta
import azure.functions as func

from dotenv import load_dotenv

load_dotenv()

# Configuración de variables de entorno
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/me/player/recently-played?limit=50'
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

# Conexión a la base de datos
DB_SERVER = os.getenv("AZURE_SERVER")
DB_DATABASE = os.getenv("DATABASE")
DB_USERNAME = os.getenv("AZURE_USER")
DB_PASSWORD = os.getenv("AZURE_PASSWORD")

session = {
    'access_token': None,
    'expires_at': None
}

app = func.FunctionApp()

@app.schedule(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False)
def SpotifyTrigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Ejecutando la función programada de Spotify...')

    # Verificar si el token ha expirado y refrescarlo si es necesario
    if session['access_token'] is None or session['expires_at'] < datetime.now().timestamp():
        logging.info('El token ha expirado o no está presente. Refrescando token...')
        refresh_access_token()

    if session['access_token']:
        headers = {
            'Authorization': f"Bearer {session['access_token']}",
        }

        response = requests.get(API_BASE_URL, headers=headers)

        if response.status_code == 200:
            data = response.json()
            insert_into_db(data)  # Llamar a la función para insertar en la base de datos
        else:
            logging.error(f"Error al obtener los tracks: {response.status_code}")
    else:
        logging.error("No se pudo obtener el token de acceso.")

# Función para refrescar el token de acceso
def refresh_access_token():
    request_body = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    response = requests.post(TOKEN_URL, data=request_body)

    if response.status_code == 200:
        token_info = response.json()
        session['access_token'] = token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        logging.info('Token de acceso refrescado correctamente.')
    else:
        logging.error(f"Error al refrescar el token: {response.status_code}")

# Función para insertar los datos en la base de datos
def round_to_nearest_millisecond(dt):
    ms = dt.microsecond // 1000  # Obtener los milisegundos
    remainder = dt.microsecond % 1000  # Obtener los microsegundos restantes

    # Si el valor de los microsegundos es mayor o igual a 500, redondeamos hacia arriba
    if remainder >= 500:
        dt += timedelta(milliseconds=1)

    # Devolver la fecha con los microsegundos ajustados
    return dt.replace(microsecond=ms * 1000)

def insert_into_db(data):
    try:
        # Conectar a la base de datos
        connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USERNAME};PWD={DB_PASSWORD}"
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Procesar cada cancion en el JSON
        for item in data['items']:
            track = item['track']
            album = track['album']
            artist = track['artists'][0]
            played_at = item['played_at']

            # Extraer los datos del track
            track_id = track['id']
            track_name = track['name']
            track_popularity = track['popularity']
            track_preview_url = track.get('preview_url', None)
            track_duration_ms = track['duration_ms']
            track_explicit = track['explicit']
            track_is_local = track['is_local']
            track_external_url = track['external_urls']['spotify']
            track_href = track['href']
            track_uri = track['uri']
            isrc = track['external_ids'].get('isrc', None)

            # Datos del álbum
            track_album_id = album['id']
            track_album_name = album['name']
            track_album_type = album['album_type']
            track_album_total_tracks = album['total_tracks']
            track_album_release_date = album['release_date']
            track_album_release_precision = album['release_date_precision']
            track_album_uri = album['uri']
            track_album_href = album['href']
            track_album_external_url = album['external_urls']['spotify']

            # Datos del artista
            track_artist_id = artist['id']
            track_artist_name = artist['name']
            track_artist_href = artist['href']
            track_artist_uri = artist['uri']
            track_artist_external_url = artist['external_urls']['spotify']

            # Formatear la fecha de 'played_at' a un formato datetime
            played_at_datetime = datetime.strptime(played_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            played_at_like_str = played_at_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # Comprobar si la combinación de track_id y played_at ya existe (pk)
            cursor.execute("""
                SELECT 1 FROM user_tracks WHERE track_id = ? AND FORMAT(played_at, 'yyyy-MM-dd HH:mm:ss') = ?
            """, (track_id, played_at_like_str))
            print(f"Selecting track {track_id} with datetime {played_at_like_str}")
            exists = cursor.fetchone()

            if exists:
                logging.info(f"Track {track_id} ya existe en la base de datos con played_at {played_at_like_str}, saltando.")
                continue
            print((f"Track {track_id} played_at {played_at_like_str}, saltando."))
            
            logging.info(f"Insertando el track {track_id} en la base de datos.")
            cursor.execute("""
                INSERT INTO user_tracks (
                    track_id, 
                    track_name, 
                    track_popularity, 
                    track_preview_url, 
                    track_duration_ms, 
                    track_explicit,
                    track_is_local, 
                    track_external_url, 
                    track_href, 
                    track_uri, 
                    track_album_id, 
                    track_album_name,
                    track_album_type, 
                    track_album_total_tracks, 
                    track_album_release_date, 
                    track_album_release_precision,
                    track_album_uri, 
                    track_album_href, 
                    track_album_external_url, 
                    track_artist_id, 
                    track_artist_name,
                    track_artist_href, 
                    track_artist_uri, 
                    track_artist_external_url, 
                    played_at, 
                    isrc
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                track_id, track_name, track_popularity, track_preview_url, track_duration_ms, track_explicit,
                track_is_local, track_external_url, track_href, track_uri, track_album_id, track_album_name,
                track_album_type, track_album_total_tracks, track_album_release_date, track_album_release_precision,
                track_album_uri, track_album_href, track_album_external_url, track_artist_id, track_artist_name,
                track_artist_href, track_artist_uri, track_artist_external_url, played_at_datetime, isrc
            ))

        conn.commit()

    except Exception as e:
        logging.error(f"Error al insertar en la base de datos: {e}")

    finally:
        conn.close()
