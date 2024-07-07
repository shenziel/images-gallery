"""Module providing a function printing python version."""

import os
import requests
from flask import Flask, request, jsonify
from dotenv import dotenv_values
from flask_cors import CORS
from mongo_client import mongo_client

gallery = mongo_client.gallery
images_collection = gallery.images

config = {
    **os.environ,  # override loaded values with environment variables
    **dotenv_values(".env.local"),
}

UNSPLASH_URL = "https://api.unsplash.com/photos/random"
UNSPLASH_KEY = config.get("UNSPLASH_KEY", "")
DEBUG = bool(config.get("DEBUG", True))

if not UNSPLASH_KEY:
    raise EnvironmentError(
        "Please create .env.local file and insert there UNSPLASH_KEY value"
    )
app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = DEBUG

@app.route("/new-image")
def new_image():
    word = request.args.get("query")
    # return {"word": word}
    headers = {
        "Accept-Version": "v1",
        "Authorization": "Client-ID " + UNSPLASH_KEY,
        "Access-control-allow-origin": "*",
    }
    params = {"query": word}
    response = requests.get(
        url=UNSPLASH_URL, headers=headers, params=params, timeout=9999
    )
    data = response.json()

    return data

@app.route("/images", methods=["GET", "POST"])
def images():
    if request.method == "GET":
        #read images from the database
        images = images_collection.find({})
        return jsonify([img for img in images])
    if request.method == "POST":
        #save image in the database
        image = request.get_json()
        image["_id"] = image.get("id")
        result = images_collection.insert_one(image)
        inserted_id = result.inserted_id
        return {"inserted_id": inserted_id}
    

@app.route("/images/<image_id>", methods=["DELETE"])
def image(image_id):
    if request.method == "DELETE":
        #delete image from the database
        result = images_collection.delete_one({"_id": image_id})
        print(result.deleted_count)
        if not result:
            return {"error": "Image wasn't deleted. Please Try again"}, 500
        if result and not result.deleted_count:
            return {"error": "Image not found"}, 404
        return {"deleted_id": image_id}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
