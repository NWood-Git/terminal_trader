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

    def test_save_insert(self):
        tester = Position(account_pk = jimid, total_quantity = 10, ticker = "pton")
        tester.save()
        result = Position.all()
        self.assertEqual(len(result),2, "len =2 b/c seeded 1 pos and added another")
        self.assertEqual(result[0].ticker,"aapl","all func populates attributes, checking first for row[0] / pk1" )
        self.assertEqual(result[1].ticker,"pton","all func populates attributes, checking email for row[1] / pk2" )
    
    def test_save_update(self):
        result = Position.from_pk(jimid)
        result.total_quantity = 12
        result.save()
        result = Position.all()
        self.assertEqual(result[0].total_quantity,12,"all func populates attributes, checking updated first for row[0] / pk1" )

    def test_all(self):
        result = Position.all()
        self.assertEqual(len(result), 1, "all func returns list with correct number of elements 1 is from seed")
        self.assertIsInstance(result[0], Position, "all func returns position object")
        self.assertEqual(result[0].total_quantity, 5, "all func populates attributes")

    # # def all_from_account(cls, account_pk)
    def test_all_from_account(self):
        result = Position.all_from_account(jimid)
        self.assertEqual(len(result), 1, "all_from_account  func returns list with correct number of elements 1 is from seed")
        self.assertIsInstance(result[0], Position, "all_from_account func returns position object")
        self.assertEqual(result[0].total_quantity, 5, "all_from_account func populates attributes")

    def test_from_account_and_ticker(self):
        result = Position.from_account_and_ticker(jimid, 'aapl')
        self.assertEqual(result.ticker,'aapl',"there was one position added by seed")
        self.assertEqual(result.total_quantity,5)
        self.assertIsInstance(result,Position,"func returns position object")