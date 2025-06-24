import mysql.connector
from config import db_config

def get_connection():
    return mysql.connector.connect(**db_config)


def execute_query(query, params=None, fetch=False, return_lastrowid=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall() if fetch else None
    lastrowid = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()

    if return_lastrowid:
        return lastrowid
    return result
