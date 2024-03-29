import os
import requests
import json
from flask_cors import CORS
from flask import Flask, request
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env.local")


UNSPLASH_URL = "https://api.unsplash.com/photos/random"
UNSPLASH_KEY = os.environ.get("UNSPLASH_KEY", "")
DEBUG = bool(os.environ.get("DEBUG", True))
APIC_USER = os.environ.get("APIC_USER", "admin")
APIC_PASSWORD = os.environ.get("APIC_PASSWORD", "C1sc0123")
APIC_URL = os.environ.get("APIC_URL", "10.138.159.34")

if not UNSPLASH_KEY:
    raise EnvironmentError(
        "Please create .env.local file and insert there UNSPLASH_KEY")

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = DEBUG


@app.route("/")
def home():
    return "Hello, world!"


@app.route("/new-image")
def new_image():
    '''API to retrieve an image randomly or from search field'''
    word = request.args.get("query")
    headers = {
        "Accept-Version": "v1",
        "Authorization": "Client-ID " + UNSPLASH_KEY
    }
    params = {
        "query": word
    }
    response = requests.get(url=UNSPLASH_URL, headers=headers, params=params)
    data = response.json()
    return data


@app.route("/apic-authen", methods=['POST'])
def api_authen():
    '''Return cookies after apic authentication'''

    credentials = {
        'aaaUser':
        {
            'attributes': {
                'name': f"{APIC_USER}",
                'pwd': f"{APIC_PASSWORD}"
            }
        }
    }
    base_url = 'https://%s/api/' % APIC_URL
    login_url = base_url + 'aaaLogin.json'
    json_credentials = json.dumps(credentials)
    post_response = requests.post(
        login_url, data=json_credentials, verify=False)
    post_response_json = json.loads(post_response.text)
    login_attributes = post_response_json['imdata'][0]['aaaLogin']['attributes']
    cookies = {}
    cookies['APIC-Cookie'] = login_attributes['token']

    return cookies["APIC-Cookie"]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
