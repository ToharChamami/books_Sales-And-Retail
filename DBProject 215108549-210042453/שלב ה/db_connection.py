import psycopg2
from psycopg2 import Error

def get_connection():
    """פונקציה שיוצרת ומחזירה חיבור לבסיס הנתונים"""
    try:
        connection = psycopg2.connect(
            user="ToharEden",       # תוקן לשם המשתמש שלך
            password="ToharEden",   # תוקן לסיסמה שלך
            host="127.0.0.1",
            port="5432",
            database="booksDB"      # תוקן לשם הדאטה-בייס שלך
        )
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("✅ Connection to PostgreSQL DB successful!")
        conn.close()