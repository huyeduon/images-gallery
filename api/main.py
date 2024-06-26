import os
import requests
import json
from flask_cors import CORS
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from mongo_client import mongo_client

# create mongodb database
gallery = mongo_client.gallery

# create images collection in gallery database
images_collection = gallery.images

load_dotenv(dotenv_path="./.env.local")

UNSPLASH_URL = "https://api.unsplash.com/photos/random"
UNSPLASH_KEY = os.environ.get("UNSPLASH_KEY", "")
DEBUG = bool(os.environ.get("DEBUG", True))
APIC_USER = os.environ.get("APIC_USER", "admin")
APIC_PASSWORD = os.environ.get("APIC_PASSWORD", "")
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


@app.route("/images", methods=["GET", "POST"])
def images():
    """
    If method GET -> read all images from database
    """
    if request.method == "GET":
        # reads image from database
        images = images_collection.find({})
        return jsonify([img for img in images])

    if request.method == "POST":
        # save image to the database
        image = request.get_json()
        image["_id"] = image.get("id")
        result = images_collection.insert_one(image)
        inserted_id = result.inserted_id
        return {"inserted_id": inserted_id}


@app.route("/images/<image_id>", methods=["DELETE"])
def image(image_id):
    if request.method == "DELETE":
        # delete image from the database
        result = images_collection.delete_one({"_id": image_id})
        if not result:
            return {"error": "Image was not deleted. Please try again"}, 500
        if result and not result.deleted_count:
            return {"error": "Image not found"}, 404
        return {"deleted_id": image_id}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
