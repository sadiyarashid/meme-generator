# Meme Generator

# Run

## Locally on your machine

### Install Prerequisite

Install all dependencies given in the requirements.txt file using pip:

```bash
$ pip install -r requirements.txt
```

Download `pdftoteext` from [here](https://www.xpdfreader.com/download.html) and make sure it's available in your `PATH`. `subprocess.run(...)` in the `memeengine/generator` will call this command line tool

```bash
$ PATH=$PATH:<PATH_TO_PDFTOTEXT>

# meme cli
$ ./meme.py
./tmp/temp-1.jpg

# web application
$ ./app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [25/Apr/2021 11:24:09] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:09] "GET /static/temp-1.jpg HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:10] "GET /favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [25/Apr/2021 11:24:11] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:11] "GET /static/temp-2.jpg HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:12] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:12] "GET /static/temp-3.jpg HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:12] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:12] "GET /static/temp-4.jpg HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:12] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:12] "GET /static/temp-5.jpg HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:12] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:12] "GET /static/temp-6.jpg HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:13] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [25/Apr/2021 11:24:13] "GET /static/temp-7.jpg HTTP/1.1" 200 -
```

## Using Docker

```bash
# build docker image
$ docker build -t app .

# meme cli
$ docker run -ti -p 8000:8000 --entrypoint /bin/bash app
$ root@9897551a94d9:/app# ./meme.py
./tmp/temp-1.jpg

# web application
$ docker run -ti -p 8000:8000 app
[2021-04-26 02:47:24 +0000] [1] [INFO] Starting gunicorn 20.1.0
[2021-04-26 02:47:24 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
[2021-04-26 02:47:24 +0000] [1] [INFO] Using worker: sync
[2021-04-26 02:47:24 +0000] [8] [INFO] Booting worker with pid: 8
```

After running the above image, web app should be accessible on `localhost:5000` (Local) /  `localhost:8000` (Docker)


# Quote Engine Module

This module reads quotes from various files and returns a list of processed quotes.

## Interface: Ingestor
This class is an interface that is used as a base class for all other ingestors. It has a complete class method `verify` that checks if a file extension is supported or not. It has an abstract class method `parse` that is used by the derived classes to parse files.

## Class: CSVIngestor
As the name suggests, this ingestor overrides the `parse` method to read CSV files, extract lines and return a list of quotes. It uses the `pandas` library to read CSVs.

## Class: DocxIngestor
As the name suggests, this ingestor overrides the `parse` method to read DOCX files, extract lines and return a list of quotes. It uses the `python-docx` library to read DOCX files.

## Class: PDFIngestor
As the name suggests, this ingestor overrides the `parse` method to read PDF files and extract its lines into a text file. That text file is then parsed using the `TextIngestor` It uses the `subprocess` library to call the `pdftotext` command line tool to extract text from PDF into a `.txt` file.

## Class: TextIngestor
As the name suggests, this ingestor overrides the `parse` method to read TXT files, extract lines and return a list of quotes. It uses the in-built file reading methods to read text files.

## Class: Ingestor
This is the main class that calls all the other ingestor classes. Its `parse` method just takes the file path as an argument and it extracts the extension of the file and returns results from the required ingestor.

## Class: QuoteModel
It takes two parameters i.e. `body` and `author` of the quote. The `__repr__` method is defined for printing the value stored in this model in a human readable format.


# Meme Engine Module

This module has all the models and functions required for generating memes. Import and use `MemeEngine` class if you want to provide the image path, meme body and author yourself. Import and use `generate_meme` method if you to generate random memes. This can also be to generate custom memes. You can run this module in command line using the following command:

```
$ ./meme.py --path <path_of_the_file> --body <quote_body> --author <quote_author>
```

## Class: MemeEngine
This class takes an output directory path as an argument. Each instance keeps count of the image generated. The `make_meme` method creates the meme image and saves it in the provided output directory and returns a path to the created meme. It uses the `pillow` library to resize image and draw text on it.