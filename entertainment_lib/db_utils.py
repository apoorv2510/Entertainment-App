import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'entertainmentdb1.cx4ogu6mk4t6.us-east-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'password123',
    'database': 'entertainmentdb1'
}

def get_db_connection():
    """Establish and return a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(query, params=None):
    """Execute a query with optional parameters."""
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor
    except Error as e:
        print(f"Query execution error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
