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

jimid = None
position_pk = None
trade_pk = None 

class TestTrade(unittest.TestCase):

    def setUp(self):
        # runs before every test case
        global trade_pk
        global position_pk
        global jimid
        pks = seed.seed(TESTDBPATH)
        # trade_pk = pks['trade_pk']
        position_pk = pks['position_pk']
        jimid = pks['jimid']

    def test_dummy(self):
        '''if everything is working correctly this will pass'''
        self.assertTrue(True)

    def test_save_insert(self):
        tester = Trade(ticker = 'pton', account_pk = jimid , quantity = 10, price = 100)
        tester.save()
        result = Trade.all()
        self.assertEqual(len(result),2, "len =2 b/c seeded 1 pos and added another")
        # self.assertEqual(result[0].ticker,"aapl","all func populates attributes, checking first for row[0] / pk1" )
        # self.assertEqual(result[1].ticker,"pton","all func populates attributes, checking email for row[1] / pk2" )