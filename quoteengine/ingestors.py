#!/usr/bin/env python3
"""This module reads quotes from files and returns a list of quotes."""
import os
import subprocess

import pandas as pd
from docx import Document

from .quote_model import QuoteModel

extensions = {
    "TEXT": ".txt",
    "CSV": ".csv",
    "PDF": ".pdf",
    "DOCX": ".docx",
}


class IngestorInterface:
    """This class is an interface that is used by all other ingestors."""

    @classmethod
    def verify(cls, file_extension):
        """Check if a file extension is supported or not."""
        return file_extension in extensions.values()

    @classmethod
    def parse(cls, path):
        """Read files, extract lines and return a list of quotes."""
        pass


class CSVIngestor(IngestorInterface):
    """Read CSV files, extract lines and return a list of quotes."""

    @classmethod
    def parse(cls, path):
        """Read CSV files, extract lines and return a list of quotes."""
        csv = pd.read_csv(path)
        return [QuoteModel(**row) for index, row in csv.iterrows()]


class DocxIngestor(IngestorInterface):
    """Read DOCX files, extract lines and return a list of quotes."""

    @classmethod
    def parse(cls, path):
        """Read DOCX files, extract lines and return a list of quotes."""
        document = Document(path)
        quotes = []
        for paragraph in document.paragraphs:
            paragraph.text and quotes.append(
                QuoteModel(*paragraph.text.split(" - "))
            )
        return quotes


class PDFIngestor(IngestorInterface):
    """Read PDF files, extract lines and return a list of quotes."""

    @classmethod
    def parse(cls, path):
        """Read PDF files, extract lines and return a list of quotes."""
        text_file = "./pdf_to_text.txt"
        cmd = f"pdftotext -layout -nopgbrk {path} {text_file}"
        subprocess.run(cmd, shell=True, stderr=subprocess.STDOUT, check=True)
        quotes = TextIngestor.parse(text_file)
        os.remove(text_file)
        return quotes


class TextIngestor(IngestorInterface):
    """Read TXT files, extract lines and return a list of quotes."""

    @classmethod
    def parse(cls, path):
        """Read TXT files, extract lines and return a list of quotes."""
        file = open(path, "r", encoding="utf-8-sig")
        lines = file.readlines()
        file.close()
        x = [QuoteModel(*quote.rstrip("\n").split(" - ")) for quote in lines]
        return x


class Ingestor(IngestorInterface):
    """Extract the extension of the file and returns the results."""

    @classmethod
    def parse(cls, path):
        """Extract the extension of the file and returns the results."""
        filename, file_extension = os.path.splitext(path)
        if not cls.verify(file_extension):
            raise ValueError("Unsupported file extension:", file_extension)
        if file_extension == extensions.get("TEXT"):
            return TextIngestor.parse(path)
        if file_extension == extensions.get("DOCX"):
            return DocxIngestor.parse(path)
        if file_extension == extensions.get("PDF"):
            return PDFIngestor.parse(path)
        if file_extension == extensions.get("CSV"):
            return CSVIngestor.parse(path)
