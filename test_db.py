import pyodbc
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

AZURE_SQL_SERVER = os.environ.get('AZURE_SQL_SERVER')
AZURE_SQL_DATABASE = os.environ.get('AZURE_SQL_DATABASE')
AZURE_SQL_USERNAME = os.environ.get('AZURE_SQL_USERNAME')
AZURE_SQL_PASSWORD = os.environ.get('AZURE_SQL_PASSWORD')
AZURE_SQL_DRIVER = os.environ.get('AZURE_SQL_DRIVER', '{ODBC Driver 18 for SQL Server}')

connection_string = (
    f"Driver={AZURE_SQL_DRIVER};"
    f"Server=tcp:{AZURE_SQL_SERVER},1433;"
    f"Database={AZURE_SQL_DATABASE};"
    f"Uid={AZURE_SQL_USERNAME};"
    f"Pwd={AZURE_SQL_PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

print(f"Connecting to {AZURE_SQL_SERVER}...")
try:
    conn = pyodbc.connect(connection_string)
    print("Connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 1 * FROM sysobjects")
    row = cursor.fetchone()
    print("Query successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
