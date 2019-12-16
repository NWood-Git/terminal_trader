import unittest
from app.account import Account, InsufficientFundsError, InsufficientSharesError
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

jimid = None #inserted row
#### need to add tablename to account file 
#### need to creat class mwth all 

class TestAccount(unittest.TestCase):

    def setUp(self):
        # runs before every test case
        global jimid
        # with sqlite3.connect(Account.dbpath) as conn:
        #     cur = conn.cursor()
        #     SQL = f"DELETE FROM {Account.tablename}"
        #     cur.execute(SQL)
        #     SQL = f"""INSERT INTO {Account.tablename}(first, last, username, password_hash, balance, email) 
        #     VALUES ("Jim", "Love", "JimmyLove", null, 0, "jimmylove@gmail.com")"""
        #     cur.execute(SQL)
        #     jimid = cur.lastrowid
        pks = seed.seed(TESTDBPATH)
        jimid = pks['jimid']

    def test_dummy(self):
        '''if everything is working correctly this will pass'''
        self.assertTrue(True)

    def test_all(self):
        result = Account.all()
        self.assertEqual(len(result), 1, "all func returns list with correct number of elements")
        self.assertIsInstance(result[0], Account, "all func returns account object")
        self.assertEqual(result[0].first, "Jim", "all func populates attributes")
    
    def test_from_pk(self):
        result = Account.from_pk(jimid)
        self.assertIsInstance(result, Account, "from_pk returns an instance of an account")
        self.assertEqual(result.email,"jimmylove@gmail.com")
        self.assertIsNone(Account.from_pk(0), "from_pk returns None for bad pk")
    
    # def test_save(self):#do we test this or do we test the individual parts
    def test_insert(self):
        tester = Account(first='Homer', last='Simpson', username='HSimp', password_hash="password", balance=0,email='the_simpsons@fox.com')
        tester.save()
        result = Account.all()#using the all fucntion to count rows in DB
        self.assertEqual(len(result), 2, "The first row was the set up the new row was inserted")
        self.assertEqual(result[0].first,"Jim","all func populates attributes, checking first for row[0] / pk1" )
        self.assertEqual(result[1].email,"the_simpsons@fox.com","all func populates attributes, checking email for row[1] / pk2" )

    def test_update(self):
        result = Account.from_pk(jimid)
        result.balance = 100
        result.save()
        result = Account.all()#using the all fucntion to count rows in DB
        self.assertEqual(result[0].balance,100,"all func populates attributes, checking updated first for row[0] / pk1" )

    def test_login_attempt(self):
        result = Account.from_pk(jimid)
        result.set_password("password")
        result.save()
        test = Account.login_attempt("JimmyLove","password")
        self.assertIsNotNone(test, "login should work with the username & password")
        
    def test_buy(self):#buy is trade withe positive quantity
        acct = Account.from_pk(jimid)
        result = acct.trade("aapl", 3, 100)#result is mv of trade
        result2 = acct.trade("pton", 1, 100)
        trade_hist = Trade.from_account_and_ticker(jimid, "aapl")
        trade_hist2 = Trade.from_account_and_ticker(jimid, "pton")
        pos_test = Position.from_account_and_ticker(jimid, "aapl")
        quant = pos_test.total_quantity
        self.assertAlmostEqual(result, 300, "mv = px * quantity")
        self.assertAlmostEqual(acct.balance, 600, "balance started at 1000 trades cost 400 so new bal should be 600" )
        self.assertEqual(len(trade_hist),2,"there shouold only be 2 trades with aapl one trade here and one from seed")
        self.assertEqual(len(trade_hist2),1,"there shouold only be 1 trade with pton from here and one from seed")
        self.assertAlmostEqual(quant, 8, "seed gave 5 shs of aapl and this test bought 3 total position is now 8")
        with self.assertRaises(InsufficientFundsError):#"tring buy shs that cost more then your balance causes an error"
            result3 = acct.trade("pton",500,100)
        
    
    def test_sell(self):
        #sell is the same function, trade, as buy with negtive quantity 
        # it has opposite effect on cash balance and position
        acct = Account.from_pk(jimid)
        result = acct.trade("aapl", -2, 100)#result is mv of trade
        pos_test = Position.from_account_and_ticker(jimid, "aapl")
        quant = pos_test.total_quantity
        trade_hist = Trade.from_account_and_ticker(jimid, "aapl")
        self.assertAlmostEqual(result, 200, "mv = quantity * px")
        self.assertAlmostEqual(quant, 3, "seed gave 5 shs of aapl and this test sold 2; total position is now 3")
        self.assertAlmostEqual(acct.balance, 1200, "started with 1000 and sell give +200")
        self.assertEqual(len(trade_hist),2,"there shouold only be 2 trades with aapl one trade here and one from seed")
        with self.assertRaises(InsufficientSharesError):#"tring sell shs that you don't have causes an error"
            result3 = acct.trade("pton",-10,100)
        with self.assertRaises(InsufficientSharesError):#"tring sell more shs than you have causes an error"
            result3 = acct.trade("aapl",-20,100)

    def test_admin_fld(self):
        tester = Account(first='Test', last='Ad', username='admin', password_hash='temp', balance=0,email='admin@test.com')
        second = Account(first='Test', last='Ad', username='not_admin', password_hash='temp', balance=0,email='admin@test.com')
        tester.save()
        self.assertEqual(tester.admin,1,"username admin should make admin field 1 for true")
        self.assertEqual(second.admin,0,"this should not be admin")