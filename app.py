#!/usr/bin/env python3
"""Meme Generator Web App."""
import random
import os
import requests
from flask import Flask, render_template, abort, request

from memeengine import MemeEngine
from quoteengine import Ingestor

app = Flask(__name__)

meme = MemeEngine("./static")


def setup():
    """Load all resources."""
    quote_files = [
        "./_data/DogQuotes/DogQuotesTXT.txt",
        "./_data/DogQuotes/DogQuotesDOCX.docx",
        "./_data/DogQuotes/DogQuotesPDF.pdf",
        "./_data/DogQuotes/DogQuotesCSV.csv",
    ]

    quotes = []
    for file in quote_files:
        try:
            quotes.extend(Ingestor.parse(file))
        except ValueError as error:
            print(f"ValueError: {error}")

    images_path = "./_data/photos/dog/"

    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]
    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template("meme.html", path=path)


@app.route("/create", methods=["GET"])
def meme_form():
    """User input for meme information."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Create a user defined meme."""
    image_url = request.form.get("image_url")
    body = request.form.get("body", "")
    author = request.form.get("author", "")
    try:
        resp = requests.get(image_url, stream=True)
        image_filename = "./temp.jpg"
        with open(image_filename, "wb") as f:
            f.write(resp.content)

        path = meme.make_meme(image_filename, body, author)
        os.remove(image_filename)
        return render_template("meme.html", path=path)
    except Exception as e:
        return render_template("meme_form.html", message="Invalid Image URL")


if __name__ == "__main__":
    app.run(debug=True)
