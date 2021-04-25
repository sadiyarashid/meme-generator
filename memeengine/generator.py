#!/usr/bin/env python3

"""This module has all the models and functions for generating memes."""

import os
import random
import textwrap
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw


class MemeEngine:
    """The engine behind meme generation."""

    def __init__(self, output_dir):
        """Save and create the output directory path."""
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def make_meme(self, img_path, text, author, width=500):
        """Create a meme using the given image, text and author."""
        img = Image.open(img_path)
        image_filename = str(datetime.now().timestamp()).replace(".", "")
        outfile = os.path.join(self.output_dir, f"{image_filename}.jpg")

        image_width, image_height = img.size
        height = int(image_height * width / image_width)
        img.thumbnail((width, height))
        # Select font-family, font-size, color and position to draw text
        font1 = ImageFont.truetype("./_data/Fonts/Roboto-Bold.ttf", 30)
        font2 = ImageFont.truetype("./_data/Fonts/Roboto-Medium.ttf", 20)
        fill = (0, 0, 0)
        stroke_fill = (255, 255, 255)

        # Draw the text on image
        draw = ImageDraw.Draw(img)
        current_h, pad = random.choice(range(10, 80)), 10
        # text = "A long text test from reviewer. This is done in order to ensure that you are using text wrap to handle corner case"
        for line in textwrap.wrap(text, width=20):
            w, h = draw.textsize(line, font=font1)
            draw.text(
                (30, current_h),
                line,
                fill,
                font1,
                stroke_width=1,
                stroke_fill=stroke_fill,
                align="center"
            )
            current_h += h + pad
        draw.text(
            (40, current_h + 10),
            f"- {author}",
            fill,
            font2,
            stroke_width=1,
            stroke_fill=stroke_fill,
            align="center"
        )

        img.save(outfile, "JPEG")
        return outfile
