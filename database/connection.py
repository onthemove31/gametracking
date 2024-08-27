import sqlite3
import logging

def create_db_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        logging.info(f"Connected to database: {db_path}")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection failed: {e}")
        raise

def close_db_connection(conn):
    if conn:
        conn.close()
        logging.info("Database connection closed.")
