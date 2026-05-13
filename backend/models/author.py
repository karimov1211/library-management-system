"""
Muallif (Author) OOP klassi.
Mualliflar haqidagi ma'lumotlarni boshqarish uchun.
"""

from datetime import datetime


class Author:
    """
    Muallif klasssi - kutubxona tizimidagi mualliflarni ifodalaydi.
    
    Atributlar:
        id (int): Muallifning unikal identifikatori
        first_name (str): Muallifning ismi
        last_name (str): Muallifning familiyasi
        birth_year (int): Tug'ilgan yili
        nationality (str): Millati
        biography (str): Qisqacha tarjimai hol
        created_at (datetime): Yozuv yaratilgan vaqt
    """

    def __init__(self, first_name: str, last_name: str, birth_year: int = None,
                 nationality: str = None, biography: str = None, author_id: int = None):
        """Muallif obyektini yaratish."""
        self._id = author_id
        self._first_name = first_name
        self._last_name = last_name
        self._birth_year = birth_year
        self._nationality = nationality
        self._biography = biography
        self._created_at = datetime.now()

    # ===== PROPERTY (Xususiyatlar) =====

    @property
    def id(self) -> int:
        """Muallif IDsi."""
        return self._id

    @id.setter
    def id(self, value: int):
        if value is not None and value < 0:
            raise ValueError("ID manfiy bo'lishi mumkin emas.")
        self._id = value

    @property
    def first_name(self) -> str:
        """Muallifning ismi."""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Ism bo'sh bo'lishi mumkin emas.")
        self._first_name = value.strip()

    @property
    def last_name(self) -> str:
        """Muallifning familiyasi."""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Familiya bo'sh bo'lishi mumkin emas.")
        self._last_name = value.strip()

    @property
    def full_name(self) -> str:
        """Muallifning to'liq ismi."""
        return f"{self._first_name} {self._last_name}"

    @property
    def birth_year(self) -> int:
        return self._birth_year

    @birth_year.setter
    def birth_year(self, value: int):
        if value is not None:
            current_year = datetime.now().year
            if value < 0 or value > current_year:
                raise ValueError(f"Tug'ilgan yil 0 va {current_year} orasida bo'lishi kerak.")
        self._birth_year = value

    @property
    def nationality(self) -> str:
        return self._nationality

    @nationality.setter
    def nationality(self, value: str):
        self._nationality = value.strip() if value else None

    @property
    def biography(self) -> str:
        return self._biography

    @biography.setter
    def biography(self, value: str):
        self._biography = value

    @property
    def created_at(self) -> datetime:
        return self._created_at

    # ===== METODLAR =====

    def to_dict(self) -> dict:
        """Muallif ma'lumotlarini lug'at (dictionary) ko'rinishida qaytarish."""
        return {
            'id': self._id,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'full_name': self.full_name,
            'birth_year': self._birth_year,
            'nationality': self._nationality,
            'biography': self._biography,
            'created_at': self._created_at.isoformat() if self._created_at else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Author':
        """Lug'atdan Muallif obyektini yaratish."""
        return cls(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            birth_year=data.get('birth_year'),
            nationality=data.get('nationality'),
            biography=data.get('biography'),
            author_id=data.get('id')
        )

    @classmethod
    def from_db_row(cls, row) -> 'Author':
        """Ma'lumotlar bazasi satridan Muallif obyektini yaratish."""
        author = cls(
            first_name=row[1],
            last_name=row[2],
            birth_year=row[3],
            nationality=row[4],
            biography=row[5],
            author_id=row[0]
        )
        if len(row) > 6 and row[6]:
            author._created_at = row[6]
        return author

    def validate(self) -> list:
        """Ma'lumotlarni tekshirish. Xatolar ro'yxatini qaytaradi."""
        errors = []
        if not self._first_name or not self._first_name.strip():
            errors.append("Ism kiritilishi shart.")
        if not self._last_name or not self._last_name.strip():
            errors.append("Familiya kiritilishi shart.")
        if self._birth_year is not None:
            if self._birth_year < 0 or self._birth_year > datetime.now().year:
                errors.append("Tug'ilgan yil noto'g'ri.")
        return errors

    def __str__(self) -> str:
        return f"Muallif: {self.full_name} ({self._birth_year or 'N/A'})"

    def __repr__(self) -> str:
        return f"Author(id={self._id}, name='{self.full_name}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Author):
            return False
        return (self._first_name == other._first_name and 
                self._last_name == other._last_name)

    def __hash__(self) -> int:
        return hash((self._first_name, self._last_name))
