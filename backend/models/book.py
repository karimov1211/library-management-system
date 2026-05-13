"""
Kitob (Book) OOP klassi.
"""
from datetime import datetime


class Book:
    """Kitob klassi - kutubxonadagi kitoblarni ifodalaydi."""

    GENRES = [
        "Badiiy adabiyot", "Ilmiy", "Tarixiy", "Falsafa",
        "Texnologiya", "Tibbiyot", "Huquq", "Iqtisodiyot",
        "Pedagogika", "Psixologiya", "Boshqa"
    ]

    def __init__(self, title, isbn=None, year=None, genre=None,
                 pages=None, author_id=None, available=True,
                 quantity=1, book_id=None):
        self._id = book_id
        self._title = title
        self._isbn = isbn
        self._year = year
        self._genre = genre
        self._pages = pages
        self._author_id = author_id
        self._available = available
        self._quantity = quantity
        self._created_at = datetime.now()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not value.strip():
            raise ValueError("Kitob nomi bo'sh bo'lishi mumkin emas.")
        self._title = value.strip()

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, value):
        self._isbn = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        self._year = value

    @property
    def genre(self):
        return self._genre

    @genre.setter
    def genre(self, value):
        self._genre = value

    @property
    def pages(self):
        return self._pages

    @pages.setter
    def pages(self, value):
        self._pages = value

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        self._author_id = value

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        self._available = bool(value)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if value is not None and value < 0:
            raise ValueError("Nusxalar soni manfiy bo'lishi mumkin emas.")
        self._quantity = value

    @property
    def created_at(self):
        return self._created_at

    def borrow(self):
        """Kitobni ijaraga berish."""
        if self._available and self._quantity > 0:
            self._quantity -= 1
            if self._quantity == 0:
                self._available = False
            return True
        return False

    def return_book(self):
        """Kitobni qaytarish."""
        self._quantity += 1
        self._available = True

    def to_dict(self):
        return {
            'id': self._id, 'title': self._title, 'isbn': self._isbn,
            'year': self._year, 'genre': self._genre, 'pages': self._pages,
            'author_id': self._author_id, 'available': self._available,
            'quantity': self._quantity
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data.get('title', ''), isbn=data.get('isbn'),
            year=data.get('year'), genre=data.get('genre'),
            pages=data.get('pages'), author_id=data.get('author_id'),
            available=data.get('available', True),
            quantity=data.get('quantity', 1), book_id=data.get('id')
        )

    @classmethod
    def from_db_row(cls, row):
        return cls(
            title=row[1], isbn=row[2], year=row[3], genre=row[4],
            pages=row[5], author_id=row[6], available=bool(row[7]),
            quantity=row[8], book_id=row[0]
        )

    def validate(self):
        errors = []
        if not self._title or not self._title.strip():
            errors.append("Kitob nomi kiritilishi shart.")
        return errors

    def __str__(self):
        status = "Mavjud" if self._available else "Ijarada"
        return f"Kitob: '{self._title}' ({self._year or 'N/A'}) - {status}"

    def __repr__(self):
        return f"Book(id={self._id}, title='{self._title}')"
