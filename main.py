"""
Avtomatlashtirilgan Kutubxona Tizimi - FastAPI + Uvicorn Backend.
Version: 1.0.1
"""
import os
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from database.db_manager import DatabaseManager
from models import Author, Book, Borrower, Loan
import config

app = FastAPI(title="Library Management API")
app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

# Static va Templates yo'llari
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'templates'))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, 'static')), name="static")

db = DatabaseManager()

@app.on_event("startup")
async def startup_event():
    try:
        db.connect()
        db.create_tables()
        print("FastAPI: Azure SQL bazasiga muvaffaqiyatli ulandi!")
    except Exception as e:
        print(f"FastAPI: Bazaga ulanishda xatolik: {e}")

def get_flash_messages(request: Request):
    return request.session.pop("_messages", [])

def add_flash_message(request: Request, message: str, category: str = "info"):
    messages = request.session.get("_messages", [])
    messages.append((category, message))
    request.session["_messages"] = messages

# ==========================================
# ROUTES
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try: stats = db.get_statistics()
    except: stats = {'total_books': 0, 'available_books': 0, 'total_authors': 0, 'total_borrowers': 0, 'active_loans': 0, 'overdue_loans': 0}
    return templates.TemplateResponse(request=request, name="index.html", context={"stats": stats, "messages": get_flash_messages(request)})

@app.get("/authors", response_class=HTMLResponse)
async def authors_page(request: Request):
    return templates.TemplateResponse(request=request, name="authors.html", context={"authors": db.get_all_authors(), "messages": get_flash_messages(request)})

@app.post("/authors/add")
async def add_author(request: Request, first_name: str = Form(...), last_name: str = Form(...), birth_year: int = Form(None), nationality: str = Form(None), biography: str = Form(None)):
    author = Author(first_name=first_name, last_name=last_name, birth_year=birth_year, nationality=nationality, biography=biography)
    db.add_author(author)
    add_flash_message(request, f"Muallif '{author.full_name}' qo'shildi!", "success")
    return RedirectResponse(url="/authors", status_code=303)

@app.get("/authors/delete/{author_id}")
async def delete_author(request: Request, author_id: int):
    db.delete_author(author_id)
    add_flash_message(request, "Muallif o'chirildi!", "success")
    return RedirectResponse(url="/authors", status_code=303)

@app.get("/books", response_class=HTMLResponse)
async def books_page(request: Request):
    return templates.TemplateResponse(request=request, name="books.html", context={"books": db.get_all_books(), "authors": db.get_all_authors(), "messages": get_flash_messages(request)})

@app.post("/books/add")
async def add_book(request: Request, title: str = Form(...), isbn: str = Form(None), year: int = Form(None), genre: str = Form(None), pages: int = Form(None), author_id: int = Form(None), quantity: int = Form(1)):
    book = Book(title=title, isbn=isbn, year=year, genre=genre, pages=pages, author_id=author_id, quantity=quantity)
    db.add_book(book)
    add_flash_message(request, f"Kitob '{book.title}' qo'shildi!", "success")
    return RedirectResponse(url="/books", status_code=303)

@app.get("/books/delete/{book_id}")
async def delete_book(request: Request, book_id: int):
    db.delete_book(book_id)
    add_flash_message(request, "Kitob o'chirildi!", "success")
    return RedirectResponse(url="/books", status_code=303)

@app.get("/api/books/search")
async def api_search_books(q: str = ""):
    books = db.search_books(q) if q else db.get_all_books()
    return {"success": True, "data": [b.to_dict() for b in books]}

@app.get("/borrowers", response_class=HTMLResponse)
async def borrowers_page(request: Request):
    return templates.TemplateResponse(request=request, name="borrowers.html", context={"borrowers": db.get_all_borrowers(), "messages": get_flash_messages(request)})

@app.post("/borrowers/add")
async def add_borrower(request: Request, first_name: str = Form(...), last_name: str = Form(...), email: str = Form(None), phone: str = Form(None), address: str = Form(None)):
    borrower = Borrower(first_name=first_name, last_name=last_name, email=email, phone=phone, address=address)
    db.add_borrower(borrower)
    add_flash_message(request, f"Ijarachchi '{borrower.full_name}' qo'shildi!", "success")
    return RedirectResponse(url="/borrowers", status_code=303)

@app.get("/loans", response_class=HTMLResponse)
async def loans_page(request: Request):
    return templates.TemplateResponse(request=request, name="loans.html", context={"loans": db.get_all_loans(), "books": db.get_all_books(), "borrowers": db.get_all_borrowers(), "messages": get_flash_messages(request)})

@app.post("/loans/add")
async def add_loan(request: Request, book_id: int = Form(...), borrower_id: int = Form(...)):
    loan = Loan(book_id=book_id, borrower_id=borrower_id)
    db.add_loan(loan)
    add_flash_message(request, "Ijara yaratildi!", "success")
    return RedirectResponse(url="/loans", status_code=303)

@app.get("/loans/return/{loan_id}")
async def return_loan(request: Request, loan_id: int):
    db.return_loan(loan_id)
    add_flash_message(request, "Kitob qaytarildi!", "success")
    return RedirectResponse(url="/loans", status_code=303)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
