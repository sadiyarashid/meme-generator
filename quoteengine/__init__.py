"""This module reads quotes from files and returns a list of quotes."""
from .quote_model import QuoteModel
from .ingestors import *


__all__ = [
    Ingestor,
    CSVIngestor,
    DocxIngestor,
    CSVIngestor,
    PDFIngestor,
    TextIngestor
]
