"""
Kutubxona tizimi modellari.
OOP klasslari: Kitob, Muallif, Ijarachchi, Ijara.
"""

from .author import Author
from .book import Book
from .borrower import Borrower
from .loan import Loan

__all__ = ['Author', 'Book', 'Borrower', 'Loan']
