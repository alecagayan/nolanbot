
from sqlite3 import connect

DB_PATH = "./data/db/database.db"

class Database():
    def __init__(self):
        pass

    def fetch_all_cars(self):
        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
        cur.execute("SELECT * FROM cars")
        rows = cur.fetchall()
        cur.close()
        db.close()
        return rows

    def query_cars(self, model):
        db = connect(DB_PATH, check_same_thread=False)
        cur = db.cursor()
        cur.execute(f"""
            SELECT *
            FROM cars
            WHERE Car LIKE '%{model}%';
        """)
        rows = cur.fetchall()
        cur.close()
        db.close()
        return rows