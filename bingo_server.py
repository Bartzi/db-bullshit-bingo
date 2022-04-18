import io
import json
import tempfile

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

    with tempfile.NamedTemporaryFile() as f:
        rendered_image.save(f.name, format="png")
        return send_file(f.name, mimetype="image/png")
