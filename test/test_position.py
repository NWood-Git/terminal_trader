import unittest
from app.account import Account
from app.position import Position
from app.trade import Trade
import schema
from settings import TESTDBPATH
import sqlite3
import seed

#python3 -m unittest discover test 

schema.schema(TESTDBPATH)
Account.dbpath = TESTDBPATH
Position.dbpath = TESTDBPATH
Trade.dbpath = TESTDBPATH
position_pk = None
jimid = None
#### need to add tablename to account file 
#### need to creat class mwth all 

class TestPosition(unittest.TestCase):

    def setUp(self):
        # # runs before every test case
        # global jimid
        # with sqlite3.connect(Account.dbpath) as conn:
        #     cur = conn.cursor()
        #     SQL = f"DELETE FROM {Account.tablename}"
        #     cur.execute(SQL)
        #     SQL = f"""INSERT INTO {Account.tablename}(first, last, username, password_hash, balance, email) 
        #     VALUES ("Jim", "Love", "JimmyLove", null, 0, "jimmylove@gmail.com")"""
        #     cur.execute(SQL)
        #     jimid = cur.lastrowid
        global position_pk
        global jimid
        pks = seed.seed(TESTDBPATH)
        position_pk = pks['position_pk']
        jimid = pks['jimid']

    def test_dummy(self):
        '''if everything is working correctly this will pass'''
        self.assertTrue(True)

    def test_from_pk(self):
        result = Position.from_pk(position_pk)
        self.assertIsInstance(result, Position, "pk returns instance of position")
        self.assertEqual(result.ticker,"aapl")
        self.assertIsNone(Position.from_pk(0),"Returns None for bad pk")
        # result = Account.from_pk(jimid)
        # self.assertIsInstance(result, Account, "from_pk returns an instance of an account")
        # self.assertEqual(result.email,"jimmylove@gmail.com")
        # self.assertIsNone(Account.from_pk(0), "from_pk returns None for bad pk")
