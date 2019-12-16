import sqlite3
# from settings import DBPATH
from settings import TESTDBPATH#This was updated since class
import os

def seed(dbpath = TESTDBPATH):
    with sqlite3.connect(dbpath) as conn:
        cur = conn.cursor()
        SQL = f"DELETE FROM accounts"
        cur.execute(SQL)
        SQL = f"DELETE FROM positions"
        cur.execute(SQL)
        SQL = f"""INSERT INTO accounts (first, last, username, password_hash, balance, email) 
        VALUES ("Jim", "Love", "JimmyLove", null, 1000, "jimmylove@gmail.com")"""
        cur.execute(SQL)
        jimid = cur.lastrowid
        
        SQL = f"""INSERT INTO positions(account_pk, ticker, total_quantity) 
        VALUES({jimid}, "aapl", 5);"""
        cur.execute(SQL)
        position_pk = cur.lastrowid
        #The below is new
        SQL = f"""INSERT INTO trades(ticker, account_pk, quantity, price)
                VALUES('aapl', {jimid}, 10, 100);"""
        cur.execute(SQL)
        trade_pk = cur.lastrowid
        return {"jimid":jimid, "position_pk" : position_pk, "trade_pk" : trade_pk}## if this is not returned all tests fail!
