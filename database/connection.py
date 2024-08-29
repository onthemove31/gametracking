import sqlite3
import os

def create_db_connection():
    db_path = os.getenv('DB_PATH', 'database/game_sessions.db')
    conn = sqlite3.connect(db_path)
    
    # Ensure tables are created by executing schema.sql
    execute_schema(conn)
    
    return conn

def execute_schema(conn):
    cursor = conn.cursor()

    # Read the schema.sql file and execute its contents
    schema_path = os.getenv('SCHEMA_PATH', 'database/schema.sql')
    with open(schema_path, 'r') as f:
        cursor.executescript(f.read())

    conn.commit()

# Example usage:
if __name__ == "__main__":
    conn = create_db_connection()
    conn.close()
