"""
Azure SQL Database boshqaruvchisi.
Barcha CRUD operatsiyalari shu yerda amalga oshiriladi.
"""
import pyodbc
import config
import logging

# Loglarni sozlash
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connection pooling-ni o'chirish (Azure SQL bilan ba'zida muammo tug'diradi)
pyodbc.pooling = False

class DatabaseManager:
    """
    Azure SQL bazasiga ulanish va CRUD operatsiyalarini boshqaruvchi klass.
    Singleton pattern qo'llanilgan.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def connect(self):
        """Azure SQL bazasiga ulanish (pyodbc orqali)."""
        try:
            # Azure SQL uchun pyodbc va Connection String tavsiya etiladi
            self._connection = pyodbc.connect(config.AZURE_SQL_CONNECTION_STRING)
            logger.info("Azure SQL bazasiga muvaffaqiyatli ulandi!")
            return True
        except Exception as e:
            logger.error(f"Ulanish xatosi: {e}")
            self._connection = None
            return False

    def disconnect(self):
        """Ulanishni yopish."""
        if self._connection:
            try:
                self._connection.close()
            except:
                pass
            self._connection = None

    def get_connection(self):
        """Joriy ulanishni olish va uning holatini tekshirish."""
        # Agar ulanish obyekti mavjud bo'lmasa, ulanamiz
        if not self._connection:
            if not self.connect():
                raise ConnectionError("Ma'lumotlar bazasiga ulanib bo'lmadi.")
        
        # Ulanish o'lik yoki yo'qligini tekshiramiz (select 1 orqali)
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
        except:
            logger.info("Eski ulanish uzilgan, qayta ulanishga harakat qilinmoqda...")
            if not self.connect():
                raise ConnectionError("Ma'lumotlar bazasiga ulanib bo'lmadi.")
                
        return self._connection

    def execute_query(self, query, params=None, commit=True):
        """SQL so'rovni bajarish (INSERT, UPDATE, DELETE)."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if commit:
                conn.commit()
            return cursor
        except (pyodbc.Error, ConnectionError) as e:
            # Agar ulanish xatosi bo'lsa, bir marta qayta urinib ko'ramiz
            logger.error(f"So'rovda xatolik yuz berdi: {e}. Qayta urinib ko'rilmoqda...")
            self.disconnect() # Eski ulanishni yopamiz
            conn = self.get_connection() # Qayta ulanamiz
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            if commit:
                conn.commit()
            return cursor

    def fetch_all(self, query, params=None):
        """SELECT so'rovi — barcha natijalarni olish."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except (pyodbc.Error, ConnectionError) as e:
            logger.error(f"Fetch all xatosi: {e}. Qayta urinib ko'rilmoqda...")
            self.disconnect()
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()

    def fetch_one(self, query, params=None):
        """SELECT so'rovi — bitta natijani olish."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except (pyodbc.Error, ConnectionError) as e:
            logger.error(f"Fetch one xatosi: {e}. Qayta urinib ko'rilmoqda...")
            self.disconnect()
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()

    # ==========================================
    # JADVALLARNI YARATISH
    # ==========================================

    def create_tables(self):
        """Barcha jadvallarni yaratish."""
        queries = [
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Authors' AND xtype='U')
            CREATE TABLE Authors (
                id INT IDENTITY(1,1) PRIMARY KEY,
                first_name NVARCHAR(100) NOT NULL,
                last_name NVARCHAR(100) NOT NULL,
                birth_year INT NULL,
                nationality NVARCHAR(100) NULL,
                biography NVARCHAR(MAX) NULL,
                created_at DATETIME DEFAULT GETDATE()
            )
            """,
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Books' AND xtype='U')
            CREATE TABLE Books (
                id INT IDENTITY(1,1) PRIMARY KEY,
                title NVARCHAR(255) NOT NULL,
                isbn NVARCHAR(20) NULL,
                year INT NULL,
                genre NVARCHAR(100) NULL,
                pages INT NULL,
                author_id INT NULL,
                available BIT DEFAULT 1,
                quantity INT DEFAULT 1,
                created_at DATETIME DEFAULT GETDATE(),
                FOREIGN KEY (author_id) REFERENCES Authors(id)
            )
            """,
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Borrowers' AND xtype='U')
            CREATE TABLE Borrowers (
                id INT IDENTITY(1,1) PRIMARY KEY,
                first_name NVARCHAR(100) NOT NULL,
                last_name NVARCHAR(100) NOT NULL,
                email NVARCHAR(150) NULL,
                phone NVARCHAR(20) NULL,
                address NVARCHAR(255) NULL,
                registration_date DATETIME DEFAULT GETDATE(),
                active BIT DEFAULT 1
            )
            """,
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Loans' AND xtype='U')
            CREATE TABLE Loans (
                id INT IDENTITY(1,1) PRIMARY KEY,
                book_id INT NOT NULL,
                borrower_id INT NOT NULL,
                loan_date DATETIME DEFAULT GETDATE(),
                due_date DATETIME NOT NULL,
                return_date DATETIME NULL,
                status NVARCHAR(20) DEFAULT 'active',
                FOREIGN KEY (book_id) REFERENCES Books(id),
                FOREIGN KEY (borrower_id) REFERENCES Borrowers(id)
            )
            """
        ]
        for query in queries:
            self.execute_query(query)
        print("Jadvallar muvaffaqiyatli yaratildi!")

    # ==========================================
    # AUTHORS CRUD
    # ==========================================

    def add_author(self, author):
        """Yangi muallif qo'shish."""
        query = """
            INSERT INTO Authors (first_name, last_name, birth_year, nationality, biography)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            author.first_name, author.last_name,
            author.birth_year, author.nationality, author.biography
        ), commit=False)
        row = cursor.fetchone()
        if row:
            author.id = row[0]
        self.get_connection().commit()
        return author

    def get_all_authors(self):
        """Barcha mualliflarni olish."""
        from models.author import Author
        rows = self.fetch_all("SELECT * FROM Authors ORDER BY last_name")
        return [Author.from_db_row(row) for row in rows]

    def get_author(self, author_id):
        """Muallifni ID bo'yicha olish."""
        from models.author import Author
        row = self.fetch_one("SELECT * FROM Authors WHERE id = ?", (author_id,))
        return Author.from_db_row(row) if row else None

    def update_author(self, author):
        """Muallif ma'lumotlarini yangilash."""
        query = """
            UPDATE Authors SET first_name=?, last_name=?, birth_year=?,
            nationality=?, biography=? WHERE id=?
        """
        self.execute_query(query, (
            author.first_name, author.last_name, author.birth_year,
            author.nationality, author.biography, author.id
        ))

    def delete_author(self, author_id):
        """Muallifni o'chirish."""
        self.execute_query("DELETE FROM Authors WHERE id = ?", (author_id,))

    # ==========================================
    # BOOKS CRUD
    # ==========================================

    def add_book(self, book):
        """Yangi kitob qo'shish."""
        query = """
            INSERT INTO Books (title, isbn, year, genre, pages, author_id, available, quantity)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            book.title, book.isbn, book.year, book.genre,
            book.pages, book.author_id, book.available, book.quantity
        ), commit=False)
        row = cursor.fetchone()
        if row:
            book.id = row[0]
        self.get_connection().commit()
        return book

    def get_all_books(self):
        """Barcha kitoblarni olish."""
        from models.book import Book
        query = """
            SELECT b.*, a.first_name + ' ' + a.last_name as author_name
            FROM Books b LEFT JOIN Authors a ON b.author_id = a.id
            ORDER BY b.title
        """
        rows = self.fetch_all(query)
        books = []
        for row in rows:
            book = Book.from_db_row(row)
            book._author_name = row[-1] if row[-1] else "Noma'lum"
            books.append(book)
        return books

    def get_book(self, book_id):
        """Kitobni ID bo'yicha olish."""
        from models.book import Book
        row = self.fetch_one("SELECT * FROM Books WHERE id = ?", (book_id,))
        return Book.from_db_row(row) if row else None

    def update_book(self, book):
        """Kitob ma'lumotlarini yangilash."""
        query = """
            UPDATE Books SET title=?, isbn=?, year=?, genre=?,
            pages=?, author_id=?, available=?, quantity=? WHERE id=?
        """
        self.execute_query(query, (
            book.title, book.isbn, book.year, book.genre,
            book.pages, book.author_id, book.available, book.quantity, book.id
        ))

    def delete_book(self, book_id):
        """Kitobni o'chirish."""
        self.execute_query("DELETE FROM Books WHERE id = ?", (book_id,))

    def search_books(self, keyword):
        """Kitoblarni qidirish."""
        from models.book import Book
        query = """
            SELECT * FROM Books
            WHERE title LIKE ? OR isbn LIKE ? OR genre LIKE ?
        """
        pattern = f"%{keyword}%"
        rows = self.fetch_all(query, (pattern, pattern, pattern))
        return [Book.from_db_row(row) for row in rows]

    # ==========================================
    # BORROWERS CRUD
    # ==========================================

    def add_borrower(self, borrower):
        """Yangi ijarachchi qo'shish."""
        query = """
            INSERT INTO Borrowers (first_name, last_name, email, phone, address)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            borrower.first_name, borrower.last_name,
            borrower.email, borrower.phone, borrower.address
        ), commit=False)
        row = cursor.fetchone()
        if row:
            borrower.id = row[0]
        self.get_connection().commit()
        return borrower

    def get_all_borrowers(self):
        """Barcha ijarachchilarni olish."""
        from models.borrower import Borrower
        rows = self.fetch_all("SELECT * FROM Borrowers ORDER BY last_name")
        return [Borrower.from_db_row(row) for row in rows]

    def get_borrower(self, borrower_id):
        """Ijaracchini ID bo'yicha olish."""
        from models.borrower import Borrower
        row = self.fetch_one("SELECT * FROM Borrowers WHERE id = ?", (borrower_id,))
        return Borrower.from_db_row(row) if row else None

    def update_borrower(self, borrower):
        """Ijarachchi ma'lumotlarini yangilash."""
        query = """
            UPDATE Borrowers SET first_name=?, last_name=?, email=?,
            phone=?, address=?, active=? WHERE id=?
        """
        self.execute_query(query, (
            borrower.first_name, borrower.last_name, borrower.email,
            borrower.phone, borrower.address, borrower.active, borrower.id
        ))

    def delete_borrower(self, borrower_id):
        """Ijaracchini o'chirish."""
        self.execute_query("DELETE FROM Borrowers WHERE id = ?", (borrower_id,))

    # ==========================================
    # LOANS CRUD
    # ==========================================

    def add_loan(self, loan):
        """Yangi ijara yaratish."""
        query = """
            INSERT INTO Loans (book_id, borrower_id, loan_date, due_date, status)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self.execute_query(query, (
            loan.book_id, loan.borrower_id,
            loan.loan_date, loan.due_date, loan.status
        ), commit=False)
        row = cursor.fetchone()
        if row:
            loan.id = row[0]
        
        # Kitob mavjudligini yangilash
        self.execute_query(
            "UPDATE Books SET quantity = quantity - 1 WHERE id = ?", (loan.book_id,), commit=False
        )
        self.execute_query(
            "UPDATE Books SET available = CASE WHEN quantity > 0 THEN 1 ELSE 0 END WHERE id = ?",
            (loan.book_id,), commit=False
        )
        self.get_connection().commit()
        return loan

    def return_loan(self, loan_id):
        """Kitobni qaytarish."""
        from datetime import datetime
        loan_row = self.fetch_one("SELECT * FROM Loans WHERE id = ?", (loan_id,))
        if loan_row:
            self.execute_query(
                "UPDATE Loans SET return_date = ?, status = 'returned' WHERE id = ?",
                (datetime.now(), loan_id)
            )
            self.execute_query(
                "UPDATE Books SET quantity = quantity + 1, available = 1 WHERE id = ?",
                (loan_row[1],)
            )

    def get_all_loans(self):
        """Barcha ijaralarni olish."""
        from models.loan import Loan
        query = """
            SELECT l.*, b.title as book_title,
                   br.first_name + ' ' + br.last_name as borrower_name
            FROM Loans l
            JOIN Books b ON l.book_id = b.id
            JOIN Borrowers br ON l.borrower_id = br.id
            ORDER BY l.loan_date DESC
        """
        rows = self.fetch_all(query)
        loans = []
        for row in rows:
            loan = Loan.from_db_row(row)
            loan._book_title = row[7] if len(row) > 7 else ""
            loan._borrower_name = row[8] if len(row) > 8 else ""
            loans.append(loan)
        return loans

    def get_active_loans(self):
        """Faol ijaralarni olish."""
        from models.loan import Loan
        query = """
            SELECT l.*, b.title, br.first_name + ' ' + br.last_name
            FROM Loans l
            JOIN Books b ON l.book_id = b.id
            JOIN Borrowers br ON l.borrower_id = br.id
            WHERE l.status = 'active'
            ORDER BY l.due_date
        """
        rows = self.fetch_all(query)
        loans = []
        for row in rows:
            loan = Loan.from_db_row(row)
            loan._book_title = row[7]
            loan._borrower_name = row[8]
            loans.append(loan)
        return loans

    # ==========================================
    # STATISTIKA
    # ==========================================

    def get_statistics(self):
        """Kutubxona statistikasini olish."""
        stats = {}
        stats['total_books'] = self.fetch_one(
            "SELECT COUNT(*) FROM Books")[0]
        stats['available_books'] = self.fetch_one(
            "SELECT COUNT(*) FROM Books WHERE available = 1")[0]
        stats['total_authors'] = self.fetch_one(
            "SELECT COUNT(*) FROM Authors")[0]
        stats['total_borrowers'] = self.fetch_one(
            "SELECT COUNT(*) FROM Borrowers WHERE active = 1")[0]
        stats['active_loans'] = self.fetch_one(
            "SELECT COUNT(*) FROM Loans WHERE status = 'active'")[0]
        stats['overdue_loans'] = self.fetch_one(
            "SELECT COUNT(*) FROM Loans WHERE status = 'active' AND due_date < GETDATE()")[0]
        return stats
