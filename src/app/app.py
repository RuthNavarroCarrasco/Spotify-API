import requests
import os
import urllib.parse
from datetime import datetime
from flask import Flask, redirect, request, jsonify, session, render_template

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.secret_key = '53d355f8-571a-4590-a310-1f9579440851'

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'


@app.route('/')
def index():
    # return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"
    return render_template('index.html')

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-top-read'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True # it is set to true for TESTING
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/wrapped')
def wrapped():
    return render_template('wrapped.html')

@app.route('/callback')
def callback():
    print('I got here')
    if 'error' in request.args:
        error = jsonify({"error": request.args['error']})
        print(f'I got here to the error {error}')

        return jsonify({"error": request.args['error']})

    if 'code' in request.args:
        # build a request body so we can get back the access token
        request_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=request_body)
        token_info = response.json()
        print(f'I got here to the token {token_info}')
        session['access_token'] = token_info['access_token'] # make a req to spotidfy api
        session['refresh_token'] = token_info['refresh_token'] # refresh access token when it expires
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in'] # num of seconds the access token lasts

        return redirect('/wrapped')
    
@app.route('/playlists')
def get_playlists():
    print('I reached playlist')
    if 'access_token' not in session:
        print('I reached playlist access_token not in session')
        redirect('/login')
    if 'access_token' in session and datetime.now().timestamp() > session['expires_at']:
        print('I reached playlist access_token has expired')
        return redirect('/refresh-token')
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    print('We are getting the playlists')
    response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
    playlists = response.json()

    # Construir la tabla HTML
    table = '<table border="1">'
    table += '<tr><th>Playlist Name</th><th>Owner</th><th>Tracks</th><th>Link</th></tr>'

    for playlist in playlists['items']:
        table += '<tr>'
        table += f"<td>{playlist['name']}</td>"
        table += f"<td>{playlist['owner']['display_name']}</td>"
        table += f"<td>{playlist['tracks']['total']}</td>"
        table += f"<td><a href='{playlist['external_urls']['spotify']}'>Open in Spotify</a></td>"
        table += '</tr>'

    table += '</table>' 
    # return jsonify(playlists)<

    return table

@app.route('/top-tracks')
def get_top_tracks():
    if 'access_token' not in session:
        return redirect('/login')

    if 'access_token' in session and datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }

    params = {
        'limit': 10,  # Número de canciones que deseas obtener
        'time_range': 'medium_term'  # Opciones: 'short_term', 'medium_term', 'long_term'
    }

    # Obtener las canciones más escuchadas
    top_tracks_response = requests.get(API_BASE_URL + 'me/top/tracks', headers=headers, params=params)
    top_tracks = top_tracks_response.json()

    # Generar contenido del carrusel para top canciones
    carousel_indicators = ''
    carousel_items = ''

    for idx, track in enumerate(top_tracks['items']):
        active_class = 'active' if idx == 0 else ''
        carousel_indicators += f'''
        <button type="button" data-bs-target="#carouselTracks" data-bs-slide-to="{idx}" class="{active_class}" aria-current="true" aria-label="Slide {idx + 1}"></button>
        '''
        carousel_items += f'''
        <div class="carousel-item {active_class}">
            <div class="img-container">
                <img src="{track['album']['images'][0]['url']}" class="d-block" alt="{track['name']}">
            </div>
            <div class="carousel-caption d-none d-md-block">
                <h5>{idx + 1}. {track['name']} - {track['artists'][0]['name']}</h5>
            </div>
        </div>
        '''

    return jsonify({
        'indicators': carousel_indicators,
        'items': carousel_items
    })

@app.route('/top-artists')
def get_top_artists():
    if 'access_token' not in session:
        return redirect('/login')

    if 'access_token' in session and datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }

    params = {
        'limit': 10,  # Número de artistas que deseas obtener
        'time_range': 'medium_term'  # Opciones: 'short_term', 'medium_term', 'long_term'
    }

    # Obtener los artistas más escuchados
    top_artists_response = requests.get(API_BASE_URL + 'me/top/artists', headers=headers, params=params)
    top_artists = top_artists_response.json()

    # Generar contenido del carrusel para top artistas
    carousel_indicators = ''
    carousel_items = ''

    for idx, artist in enumerate(top_artists['items']):
        active_class = 'active' if idx == 0 else ''
        carousel_indicators += f'''
        <button type="button" data-bs-target="#carouselArtists" data-bs-slide-to="{idx}" class="{active_class}" aria-current="true" aria-label="Slide {idx + 1}"></button>
        '''
        carousel_items += f'''
        <div class="carousel-item {active_class}">
            <div class="img-container">
                <img src="{artist['images'][0]['url']}" class="d-block" alt="{artist['name']}">
            </div>
            <div class="carousel-caption d-none d-md-block">
                <h5>{idx + 1}. {artist['name']}</h5>
            </div>
        </div>
        '''

    return jsonify({
        'indicators': carousel_indicators,
        'items': carousel_items
    })

@app.route('/top-genres')
def get_top_genres():
    if 'access_token' not in session:
        return redirect('/login')

    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }

    params = {
        'limit': 50,  # Obtener más artistas para generar géneros variados
        'time_range': 'medium_term'  # Opciones: 'short_term', 'medium_term', 'long_term'
    }

    top_artists_response = requests.get(API_BASE_URL + 'me/top/artists', headers=headers, params=params)
    top_artists = top_artists_response.json()

    genres_counter = {}

    for artist in top_artists['items']:
        for genre in artist['genres']:
            if genre in genres_counter:
                genres_counter[genre] += 1
            else:
                genres_counter[genre] = 1

    top_genres = sorted(genres_counter.items(), key=lambda x: x[1], reverse=True)[:3]  # Obtener los 10 géneros más escuchados

    return jsonify(top_genres)

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        redirect('/login')
    if datetime.now().timestamp() > session['expires_at']:
        print('Refreshing token')
        # make a request to get a fresh access token
        request_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=request_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        # return redirect('/playlists')
        return redirect('/top-artists')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)