import io
import json

from flask import Flask, send_file
from PIL import Image

from bingo import create_bingo

app = Flask(__name__)

with open("config.json", "rb") as f:
    config = json.load(f)

bingo_image = Image.open(config["image_path"])
bingo_items = config["bingo_items"]

@app.route("/")
def main():
    rendered_image = create_bingo(bingo_image.copy(), bingo_items)

    saved_image = io.BytesIO()
    rendered_image.save(saved_image, format="png")
    saved_image.seek(0)
    return send_file(saved_image, mimetype="image/png")
