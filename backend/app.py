"""
Avtomatlashtirilgan Kutubxona Tizimi - Flask Web Ilovasi.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from database.db_manager import DatabaseManager
from models import Author, Book, Borrower, Loan
import os
import config

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'templates')
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = config.SECRET_KEY

db = DatabaseManager()


@app.route('/')
def index():
    """Bosh sahifa — statistika."""
    try:
        stats = db.get_statistics()
    except Exception:
        stats = {
            'total_books': 0, 'available_books': 0,
            'total_authors': 0, 'total_borrowers': 0,
            'active_loans': 0, 'overdue_loans': 0
        }
    return render_template('index.html', stats=stats)


# ==========================================
# MUALLIFLAR (AUTHORS)
# ==========================================

@app.route('/authors')
def authors():
    try:
        author_list = db.get_all_authors()
    except Exception:
        author_list = []
        flash("Ma'lumotlar bazasiga ulanishda xatolik!", "error")
    return render_template('authors.html', authors=author_list)


@app.route('/authors/add', methods=['POST'])
def add_author():
    author = Author(
        first_name=request.form.get('first_name', ''),
        last_name=request.form.get('last_name', ''),
        birth_year=int(request.form['birth_year']) if request.form.get('birth_year') else None,
        nationality=request.form.get('nationality'),
        biography=request.form.get('biography')
    )
    errors = author.validate()
    if errors:
        for e in errors:
            flash(e, "error")
    else:
        try:
            db.add_author(author)
            flash(f"Muallif '{author.full_name}' muvaffaqiyatli qo'shildi!", "success")
        except Exception as ex:
            flash(f"Xatolik: {ex}", "error")
    return redirect(url_for('authors'))


@app.route('/authors/delete/<int:author_id>')
def delete_author(author_id):
    try:
        db.delete_author(author_id)
        flash("Muallif o'chirildi!", "success")
    except Exception as ex:
        flash(f"Xatolik: {ex}", "error")
    return redirect(url_for('authors'))


# ==========================================
# KITOBLAR (BOOKS)
# ==========================================

@app.route('/books')
def books():
    try:
        book_list = db.get_all_books()
        author_list = db.get_all_authors()
    except Exception:
        book_list = []
        author_list = []
        flash("Ma'lumotlar bazasiga ulanishda xatolik!", "error")
    return render_template('books.html', books=book_list, authors=author_list)


@app.route('/books/add', methods=['POST'])
def add_book():
    book = Book(
        title=request.form.get('title', ''),
        isbn=request.form.get('isbn'),
        year=int(request.form['year']) if request.form.get('year') else None,
        genre=request.form.get('genre'),
        pages=int(request.form['pages']) if request.form.get('pages') else None,
        author_id=int(request.form['author_id']) if request.form.get('author_id') else None,
        quantity=int(request.form.get('quantity', 1))
    )
    errors = book.validate()
    if errors:
        for e in errors:
            flash(e, "error")
    else:
        try:
            db.add_book(book)
            flash(f"Kitob '{book.title}' muvaffaqiyatli qo'shildi!", "success")
        except Exception as ex:
            flash(f"Xatolik: {ex}", "error")
    return redirect(url_for('books'))


@app.route('/books/delete/<int:book_id>')
def delete_book(book_id):
    try:
        db.delete_book(book_id)
        flash("Kitob o'chirildi!", "success")
    except Exception as ex:
        flash(f"Xatolik: {ex}", "error")
    return redirect(url_for('books'))


@app.route('/books/search')
def search_books():
    keyword = request.args.get('q', '')
    try:
        book_list = db.search_books(keyword) if keyword else db.get_all_books()
        author_list = db.get_all_authors()
    except Exception:
        book_list = []
        author_list = []
    return render_template('books.html', books=book_list, authors=author_list, search=keyword)


@app.route('/api/books/search')
def api_search_books():
    """JSON formatida qidiruv natijalarini qaytarish (AJAX uchun)."""
    keyword = request.args.get('q', '')
    try:
        books = db.search_books(keyword) if keyword else db.get_all_books()
        # Kitob obyektlarini dictga o'tkazamiz
        return {"success": True, "data": [b.to_dict() for b in books]}
    except Exception as e:
        return {"success": False, "error": str(e)}, 500


# ==========================================
# IJARACHCHILAR (BORROWERS)
# ==========================================

@app.route('/borrowers')
def borrowers():
    try:
        borrower_list = db.get_all_borrowers()
    except Exception:
        borrower_list = []
        flash("Ma'lumotlar bazasiga ulanishda xatolik!", "error")
    return render_template('borrowers.html', borrowers=borrower_list)


@app.route('/borrowers/add', methods=['POST'])
def add_borrower():
    borrower = Borrower(
        first_name=request.form.get('first_name', ''),
        last_name=request.form.get('last_name', ''),
        email=request.form.get('email'),
        phone=request.form.get('phone'),
        address=request.form.get('address')
    )
    errors = borrower.validate()
    if errors:
        for e in errors:
            flash(e, "error")
    else:
        try:
            db.add_borrower(borrower)
            flash(f"Ijarachchi '{borrower.full_name}' qo'shildi!", "success")
        except Exception as ex:
            flash(f"Xatolik: {ex}", "error")
    return redirect(url_for('borrowers'))


@app.route('/borrowers/delete/<int:borrower_id>')
def delete_borrower(borrower_id):
    try:
        db.delete_borrower(borrower_id)
        flash("Ijarachchi o'chirildi!", "success")
    except Exception as ex:
        flash(f"Xatolik: {ex}", "error")
    return redirect(url_for('borrowers'))


# ==========================================
# IJARALAR (LOANS)
# ==========================================

@app.route('/loans')
def loans():
    try:
        loan_list = db.get_all_loans()
        book_list = db.get_all_books()
        borrower_list = db.get_all_borrowers()
    except Exception:
        loan_list = []
        book_list = []
        borrower_list = []
        flash("Ma'lumotlar bazasiga ulanishda xatolik!", "error")
    return render_template('loans.html', loans=loan_list,
                           books=book_list, borrowers=borrower_list)


@app.route('/loans/add', methods=['POST'])
def add_loan():
    loan = Loan(
        book_id=int(request.form['book_id']),
        borrower_id=int(request.form['borrower_id'])
    )
    errors = loan.validate()
    if errors:
        for e in errors:
            flash(e, "error")
    else:
        try:
            db.add_loan(loan)
            flash("Ijara muvaffaqiyatli yaratildi!", "success")
        except Exception as ex:
            flash(f"Xatolik: {ex}", "error")
    return redirect(url_for('loans'))


@app.route('/loans/return/<int:loan_id>')
def return_loan(loan_id):
    try:
        db.return_loan(loan_id)
        flash("Kitob qaytarildi!", "success")
    except Exception as ex:
        flash(f"Xatolik: {ex}", "error")
    return redirect(url_for('loans'))


# ==========================================
# ISHGA TUSHIRISH
# ==========================================

if __name__ == '__main__':
    try:
        db.connect()
        db.create_tables()
        print("Kutubxona tizimi ishga tushdi!")
    except Exception as e:
        print(f"Bazaga ulanishda xatolik: {e}")
        print("Ilova bazasiz ishga tushmoqda...")
    app.run(debug=True, host='0.0.0.0', port=5000)
