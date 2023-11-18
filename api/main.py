import os
import requests
from flask import Flask, request
from dotenv import dotenv_values

config = {
    **os.environ,  # override loaded values with environment variables
    **dotenv_values(".env.local")
}

UNSPLASH_URL="https://api.unsplash.com/photos/random"
UNSPLASH_KEY=config.get("UNSPLASH_KEY", "")
DEBUG=bool(config.get("DEBUG", True))

if not UNSPLASH_KEY:
    raise EnvironmentError("Please create .env.local file and insert there UNSPLASH_KEY value")
app = Flask(__name__)

app.config["DEBUG"] = DEBUG

@app.route("/new-image")
def new_image():
    word = request.args.get("query")
    headers = {
        "Accept-Version": "v1",
        "Authorization": "Client-ID " + UNSPLASH_KEY
    }
    params = {"query": word}
    response = requests.get(url=UNSPLASH_URL, headers=headers, params=params)
    data = response.json()

    return data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)