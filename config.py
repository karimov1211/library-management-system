"""
Kutubxona tizimi konfiguratsiyasi.
Azure SQL va Flask sozlamalari.
"""

import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)  # .env fayldan o'zgaruvchilarni yuklash

# Flask konfiguratsiyasi
SECRET_KEY = os.environ.get('SECRET_KEY', 'kutubxona-tizimi-maxfiy-kalit-2026')

# ========================================
# Azure SQL Database konfiguratsiyasi
# ========================================
# Quyidagi ma'lumotlarni Azure portalidan oling:
AZURE_SQL_SERVER = os.environ.get('AZURE_SQL_SERVER', 'your-server.database.windows.net')
AZURE_SQL_DATABASE = os.environ.get('AZURE_SQL_DATABASE', 'LibraryDB')
AZURE_SQL_USERNAME = os.environ.get('AZURE_SQL_USERNAME', 'your-username')
AZURE_SQL_PASSWORD = os.environ.get('AZURE_SQL_PASSWORD', 'your-password')
AZURE_SQL_DRIVER = os.environ.get('AZURE_SQL_DRIVER', '{ODBC Driver 18 for SQL Server}')

# Azure SQL ulanish satri (Connection String)
AZURE_SQL_CONNECTION_STRING = (
    f"Driver={AZURE_SQL_DRIVER};"
    f"Server=tcp:{AZURE_SQL_SERVER},1433;"
    f"Database={AZURE_SQL_DATABASE};"
    f"Uid={AZURE_SQL_USERNAME};"
    f"Pwd={AZURE_SQL_PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=yes;"
    f"Connection Timeout=30;"
    f"ConnectRetryCount=3;"
    f"ConnectRetryInterval=10;"
    f"MultipleActiveResultSets=True;"
)
