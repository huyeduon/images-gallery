import os
import requests
import json
from flask_cors import CORS
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from mongo_client import mongo_client


load_dotenv(dotenv_path="./.env.local")

DEBUG = bool(os.environ.get("DEBUG", True))
APIC_USER = os.environ.get("APIC_USER", "admin")
APIC_PASSWORD = os.environ.get("APIC_PASSWORD", "")
APIC_URL = os.environ.get("APIC_URL", "10.138.159.34")


app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = DEBUG


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
