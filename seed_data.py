from database.db_manager import DatabaseManager
from models.author import Author
from models.book import Book
from models.borrower import Borrower

def seed():
    db = DatabaseManager()
    db.connect()
    
    print("Bazaga ma'lumotlarni qo'shish boshlandi...")

    # 1. Mualliflar
    authors_data = [
        ("Abdulla", "Qodiriy", 1894, "O'zbek", "Zamonaviy o'zbek romanchiligining asoschisi."),
        ("Abdulhamid", "Cho'lpon", 1897, "O'zbek", "Mashhur o'zbek shoiri va yozuvchisi."),
        ("Abdurauf", "Fitrat", 1886, "O'zbek", "Jadidchilik harakatining namoyandasi."),
        ("G'afur", "G'ulom", 1903, "O'zbek", "O'zbekiston xalq shoiri."),
        ("Muso Toshmuhammad", "Oybek", 1905, "O'zbek", "Mashhur o'zbek yozuvchisi va shoiri.")
    ]
    
    author_ids = []
    for f, l, y, n, b in authors_data:
        author = Author(first_name=f, last_name=l, birth_year=y, nationality=n, biography=b)
        db.add_author(author)
        # ID ni olish uchun qayta so'raymiz (sodda usul)
        all_authors = db.get_all_authors()
        author_ids.append(all_authors[-1].id)
    print(f"5 ta muallif qo'shildi.")

    # 2. Kitoblar
    books_data = [
        ("O'tkan kunlar", "978-1234567890", 1922, "Badiiy adabiyot", 400, author_ids[0]),
        ("Kecha va kunduz", "978-0987654321", 1936, "Badiiy adabiyot", 350, author_ids[1]),
        ("Qiyomat", "978-1122334455", 1923, "Falsafa", 200, author_ids[2]),
        ("Shum bola", "978-5566778899", 1936, "Badiiy adabiyot", 150, author_ids[3]),
        ("Navoiy", "978-9988776655", 1944, "Tarixiy", 450, author_ids[4])
    ]
    
    for t, i, y, g, p, aid in books_data:
        book = Book(title=t, isbn=i, year=y, genre=g, pages=p, author_id=aid, quantity=3)
        db.add_book(book)
    print(f"5 ta kitob qo'shildi.")

    # 3. Ijarachilar
    borrowers_data = [
        ("Javohir", "Karimov", "javohir@example.com", "+998901234567", "Toshkent sh."),
        ("Malika", "Ergasheva", "malika@example.com", "+998912345678", "Samarqand sh."),
        ("Sardor", "Alimov", "sardor@example.com", "+998933456789", "Buxoro sh."),
        ("Nigora", "Yusupova", "nigora@example.com", "+998944567890", "Namangan sh."),
        ("Rustam", "Ahmedov", "rustam@example.com", "+998955678901", "Andijon sh.")
    ]
    
    for f, l, e, p, a in borrowers_data:
        borrower = Borrower(first_name=f, last_name=l, email=e, phone=p, address=a)
        db.add_borrower(borrower)
    print(f"5 ta ijarachi qo'shildi.")

    print("Barcha ma'lumotlar muvaffaqiyatli qo'shildi!")

if __name__ == "__main__":
    seed()
