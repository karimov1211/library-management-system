import sys
import os
from database.db_manager import DatabaseManager
def show_all_tables():
    db = DatabaseManager()
    
    tables = ['Authors', 'Books', 'Borrowers', 'Loans']
    
    for table in tables:
        print(f"\n--- {table} JADVALI ---")
        try:
            # Barcha ustunlarni olish
            rows = db.fetch_all(f"SELECT * FROM {table}")
            
            # Ustun nomlarini olish
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT TOP 1 * FROM {table}")
            columns = [column[0] for column in cursor.description]
            
            print(" | ".join(columns))
            print("-" * (len(" | ".join(columns))))
            
            if rows:
                for row in rows:
                    print(" | ".join(map(str, row)))
            else:
                print(f"{table} jadvali bo'sh.")
        except Exception as e:
            print(f"{table} jadvalini o'qishda xatolik: {e}")

if __name__ == "__main__":
    # Path-ni to'g'rilash
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    show_all_tables()
