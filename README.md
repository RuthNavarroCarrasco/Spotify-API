# How to run

Create a `.env` file with the following content:
```
CLIENT_ID="foo"
CLIENT_SECRET="bar"
```
Take the id and secret from your Spotify developer account.

Add this as Redirect URIs: `http://localhost:5000/callback`

```bash
poetry install
poetry shell
python3 src/app/app.py
``` 

# Spotify-API

- generos mas escuchados
- total de canciones escuchadas 
- canción que más hemos escuchado
- otras canciones.. (top 5) DONE
- total de minutos NO SE PUEDE
- dia que mas se escucho NO SE PUEDE
- total artistas que se han escuchado DONE