"""
Ijarachchi (Borrower) OOP klassi.
"""
from datetime import datetime


class Borrower:
    """Ijarachchi klassi - kutubxonaga a'zo bo'lgan foydalanuvchilarni ifodalaydi."""

    def __init__(self, first_name, last_name, email=None, phone=None,
                 address=None, borrower_id=None):
        self._id = borrower_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._phone = phone
        self._address = address
        self._registration_date = datetime.now()
        self._active = True

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or not value.strip():
            raise ValueError("Ism bo'sh bo'lishi mumkin emas.")
        self._first_name = value.strip()

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or not value.strip():
            raise ValueError("Familiya bo'sh bo'lishi mumkin emas.")
        self._last_name = value.strip()

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value and '@' not in value:
            raise ValueError("Email formati noto'g'ri.")
        self._email = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def registration_date(self):
        return self._registration_date

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = bool(value)

    def deactivate(self):
        """Ijarachchi hisobini o'chirish."""
        self._active = False

    def activate(self):
        """Ijarachchi hisobini yoqish."""
        self._active = True

    def to_dict(self):
        return {
            'id': self._id, 'first_name': self._first_name,
            'last_name': self._last_name, 'full_name': self.full_name,
            'email': self._email, 'phone': self._phone,
            'address': self._address, 'active': self._active,
            'registration_date': self._registration_date.isoformat() if self._registration_date else None
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email'), phone=data.get('phone'),
            address=data.get('address'), borrower_id=data.get('id')
        )

    @classmethod
    def from_db_row(cls, row):
        b = cls(
            first_name=row[1], last_name=row[2], email=row[3],
            phone=row[4], address=row[5], borrower_id=row[0]
        )
        if len(row) > 6 and row[6]:
            b._registration_date = row[6]
        if len(row) > 7:
            b._active = bool(row[7])
        return b

    def validate(self):
        errors = []
        if not self._first_name or not self._first_name.strip():
            errors.append("Ism kiritilishi shart.")
        if not self._last_name or not self._last_name.strip():
            errors.append("Familiya kiritilishi shart.")
        if self._email and '@' not in self._email:
            errors.append("Email formati noto'g'ri.")
        return errors

    def __str__(self):
        status = "Faol" if self._active else "Nofaol"
        return f"Ijarachchi: {self.full_name} - {status}"

    def __repr__(self):
        return f"Borrower(id={self._id}, name='{self.full_name}')"
