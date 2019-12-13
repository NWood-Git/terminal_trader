import sqlite3
from settings import DBPATH
import os

def seed(dbpath = DBPATH):
    with sqlite3.connect(dbpath) as conn:
        cur = conn.cursor()
        SQL = f"DELETE FROM accounts"
        cur.execute(SQL)
        SQL = f"DELETE FROM positions"
        cur.execute(SQL)
        SQL = f"""INSERT INTO accounts (first, last, username, password_hash, balance, email) 
        VALUES ("Jim", "Love", "JimmyLove", null, 0, "jimmylove@gmail.com")"""
        cur.execute(SQL)
        jimid = cur.lastrowid
        SQL = f"""INSERT INTO positions(account_pk, ticker, total_quantity) 
        VALUES({jimid}, "aapl", 5);"""
        cur.execute(SQL)
        position_pk = cur.lastrowid
        #DO the above for trade as well
        return {"jimid":jimid, "position_pk" : position_pk}
