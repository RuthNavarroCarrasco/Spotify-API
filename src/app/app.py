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
    return render_template('artists.html')

@app.route('/callback')
def callback():
    if 'error' in request.args:
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
        session['access_token'] = token_info['access_token'] # make a req to spotidfy api
        session['refresh_token'] = token_info['refresh_token'] # refresh access token when it expires
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in'] # num of seconds the access token lasts

        return redirect('/top')

@app.route('/top')
def get_top_tracks_and_artists():
    if 'access_token' not in session:
        return redirect('/login')

    if 'access_token' in session and datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }

    params = {
        'limit': 5,
        'time_range': 'medium_term'
    }
    top_tracks_response = requests.get(API_BASE_URL + 'me/top/tracks', headers=headers, params=params)
    top_tracks = top_tracks_response.json()

    tracks = []
    for idx, track in enumerate(top_tracks['items']):
        track_data = {
            'top_position': idx + 1,
            'name': track['name'],
            'artist': ', '.join([artist['name'] for artist in track['artists']]),
            'album': track['album']['name'],
            'image': track['album']['images'][0]['url'],
            'popularity': track['popularity']
        }
        tracks.append(track_data)

    top_artists_response = requests.get(API_BASE_URL + 'me/top/artists', headers=headers, params=params)
    top_artists = top_artists_response.json()

    artists = [
        {
            'name': artist['name'],
            'image': artist['images'][0]['url'],
            'popularity': artist['popularity'],
            'followers': artist['followers']['total'],
            'top_position': idx + 1
        }
        for idx, artist in enumerate(top_artists['items'])
    ]

    return render_template('top.html', tracks=tracks, artists=artists)



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

        return redirect('/top-artists')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)