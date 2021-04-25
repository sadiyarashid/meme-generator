#!/usr/bin/env python3

"""QuoteModel to represent encapsulate body and author."""


class QuoteModel:
    """QuoteModel to represent encapsulate body and author."""

    def __init__(self, body="", author=""):
        """Accept body and author."""
        self.body = body
        self.author = author

    def __repr__(self):
        """Value stored in this model in a human readable format."""
        return f"{self.body} - {self.author}"
