import pandas as pd
import json
import base64
import requests
import os

from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_str = client_id + ":" + client_secret

    # codificar la cadena de autenticación en bytes
    auth_bytes = auth_str.encode("utf-8")

    # base 64
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type=client_credentials"
    }

    result = requests.post(url=url, headers=headers, data=data)
    json_result = json.loads(result.content)
    print(json_result)
    return json_result

get_token()