"""
Ijara (Loan) OOP klassi.
Kitob ijara operatsiyalarini boshqarish uchun.
"""
from datetime import datetime, timedelta


class Loan:
    """Ijara klassi - kitobning ijaraga berilishini ifodalaydi."""

    DEFAULT_LOAN_DAYS = 14  # Standart ijara muddati (kun)

    def __init__(self, book_id, borrower_id, loan_date=None,
                 due_date=None, return_date=None, status="active",
                 loan_id=None):
        self._id = loan_id
        self._book_id = book_id
        self._borrower_id = borrower_id
        self._loan_date = loan_date or datetime.now()
        self._due_date = due_date or (self._loan_date + timedelta(days=self.DEFAULT_LOAN_DAYS))
        self._return_date = return_date
        self._status = status  # active, returned, overdue

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def book_id(self):
        return self._book_id

    @property
    def borrower_id(self):
        return self._borrower_id

    @property
    def loan_date(self):
        return self._loan_date

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        self._due_date = value

    @property
    def return_date(self):
        return self._return_date

    @property
    def status(self):
        return self._status

    @property
    def is_overdue(self):
        """Muddati o'tganligini tekshirish."""
        if self._status == "returned":
            return False
        return datetime.now() > self._due_date

    @property
    def days_remaining(self):
        """Qolgan kunlar soni."""
        if self._status == "returned":
            return 0
        delta = self._due_date - datetime.now()
        return max(0, delta.days)

    def return_book(self):
        """Kitobni qaytarish."""
        self._return_date = datetime.now()
        self._status = "returned"

    def extend(self, days=7):
        """Ijara muddatini uzaytirish."""
        if self._status == "active":
            self._due_date += timedelta(days=days)

    def check_overdue(self):
        """Muddati o'tganligini tekshirib statusni yangilash."""
        if self._status == "active" and self.is_overdue:
            self._status = "overdue"

    def to_dict(self):
        return {
            'id': self._id, 'book_id': self._book_id,
            'borrower_id': self._borrower_id,
            'loan_date': self._loan_date.isoformat() if self._loan_date else None,
            'due_date': self._due_date.isoformat() if self._due_date else None,
            'return_date': self._return_date.isoformat() if self._return_date else None,
            'status': self._status
        }

    @classmethod
    def from_db_row(cls, row):
        return cls(
            book_id=row[1], borrower_id=row[2], loan_date=row[3],
            due_date=row[4], return_date=row[5], status=row[6],
            loan_id=row[0]
        )

    def validate(self):
        errors = []
        if not self._book_id:
            errors.append("Kitob tanlanishi shart.")
        if not self._borrower_id:
            errors.append("Ijarachchi tanlanishi shart.")
        return errors

    def __str__(self):
        return f"Ijara #{self._id}: Kitob={self._book_id}, Status={self._status}"

    def __repr__(self):
        return f"Loan(id={self._id}, book={self._book_id}, borrower={self._borrower_id})"
