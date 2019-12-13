import unittest
from app.account import Account
from app.position import Position
from app.trade import Trade
import schema
from settings import TESTDBPATH
import sqlite3

#python3 -m unittest discover test 

schema.schema(TESTDBPATH)
Account.dbpath = TESTDBPATH
Position.dbpath = TESTDBPATH
Trade.dbpath = TESTDBPATH

jimid = None #inserted row
#### need to add tablename to account file 
#### need to creat class mwth all 

class TestTrade(unittest.TestCase):

    def setUp(self):
        # runs before every test case
        global jimid
        with sqlite3.connect(Account.dbpath) as conn:
            cur = conn.cursor()
            SQL = f"DELETE FROM {Account.tablename}"
            cur.execute(SQL)
            SQL = f"""INSERT INTO {Account.tablename}(first, last, username, password_hash, balance, email) 
            VALUES ("Jim", "Love", "JimmyLove", null, 0, "jimmylove@gmail.com")"""
            cur.execute(SQL)
            jimid = cur.lastrowid

    def test_dummy(self):
        '''if everything is working correctly this will pass'''
        self.assertTrue(True)
