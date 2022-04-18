import argparse
import random

from dataclasses import dataclass
from typing import Tuple

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


font = ImageFont.truetype("DB_Fonts/DB Sans/DB Sans Regular.otf", 40)
texts = [
    "falscher Zug wird bereitgestellt",
    "geänderte Wagenreihung",
    "Zug endet hier",
    "warten auf verspäteten Zug",
    "Zug wird umgeleitet",
    "Signalstörung",
    "Gleiswechsel",
    "Verspätung von mehr als 60 Minuten",
    "Polizeieinsatz",
    "außerplanmäßiger Halt",
    "Gegenstand auf den Gleisen",
    "Toiletten defekt",
    "Anschlusszug wartet nicht",
    "Zug fällt aus",
    "Notarzteinsatz",
    "Personenschaden"
]


@dataclass
class Box:
    left: int
    top: int
    right: int
    bottom: int

    def width(self) -> int:
        return self.right - self.left

    def height(self) -> int:
        return self.bottom - self.top


def find_best_box_for_text(text:str, draw: ImageDraw.Draw, max_width: int = 345, max_height: int = 345) -> Tuple[str, Box]:
    num_splits = 0
    while True:
        split_text = text
        split_text = split_text.rsplit(' ', maxsplit=num_splits)
        split_text = '\n'.join(split_text)

        text_box = Box(*draw.multiline_textbbox((0, 0), split_text, font=font))

        if text_box.width() <= max_width:
            return split_text, text_box

        if num_splits > 10:
            raise RuntimeError("Could not find a suitable split")

        num_splits += 1


def create_bingo(bingo_image, texts) -> Image:
    # width 345, 25 margin
    # height 345, 25 margin
    
    texts = random.sample(texts, k=16)
    draw = ImageDraw.Draw(bingo_image)
    for i, text in enumerate(texts):
        row = i // 4
        column = i % 4
        x_start = column * 345 + (column + 1) * 25 + 120
        y_start = row * 345 + (row + 1) * 25 + 855

        text, box = find_best_box_for_text(text, draw)

        center_x = x_start + 345 / 2
        center_y = y_start + 345 / 2

        x_start = center_x - box.width() / 2
        y_start = center_y - box.height() / 2

        draw.multiline_text((x_start, y_start), text, font=font, fill="black", align="center")
    return bingo_image



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bingo_image", help="Path to bino base image")
    
    args = parser.parse_args()

    with Image.open(args.bingo_image) as the_image:
        new_image = create_bingo(the_image, texts)
        new_image.show()
