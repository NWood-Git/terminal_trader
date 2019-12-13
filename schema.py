import sqlite3
from settings import DBPATH
import os


def schema(dbpath=DBPATH):
    with sqlite3.connect(dbpath) as connection:
        cursor = connection.cursor()

        DROP_SQL = "DROP TABLE IF EXISTS accounts;"
        cursor.execute(DROP_SQL)
        ##TODO: add NOT NULL to username
        SQL = """CREATE TABLE accounts(
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            first VARCHAR(128),
            last VARCHAR(128),
            username VARCHAR(128),
            password_hash VARCHAR(128),
            balance FLOAT,
            email VARCHAR(128),
            UNIQUE(username))"""
        cursor.execute(SQL)

        DROP_SQL = "DROP TABLE IF EXISTS positions;"
        cursor.execute(DROP_SQL)

        SQL = """CREATE TABLE positions(
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            account_pk INTEGER,
            total_quantity INTEGER,
            ticker VARCHAR(10) NOT NULL,
            FOREIGN KEY (account_pk) REFERENCES accounts(pk),
            UNIQUE(account_pk, ticker));"""
        cursor.execute(SQL)
        
        DROP_SQL = "DROP TABLE IF EXISTS trades"
        cursor.execute(DROP_SQL)

        SQL = """CREATE TABLE trades(
            pk INTEGER PRIMARY KEY AUTOINCREMENT,
            account_pk INTEGER, 
            ticker VARCHAR(10),
            quantity INTEGER,
            price FLOAT,
            created_at FLOAT,
            FOREIGN KEY (account_pk) REFERENCES accounts(pk))"""
        cursor.execute(SQL)

if __name__ == "__main__":
    schema()