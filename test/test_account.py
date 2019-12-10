import unittest
from app.account import Account
import schema
from settings import TESTDBPATH
import sqlite3

#python3 -m unittest discover test 

schema.schema(TESTDBPATH)
Account.dbpath = TESTDBPATH
jimid = None #inserted row
#### need to add tablename to account file 
#### need to creat class mwth all 

class TestAccount(unittest.TestCase):

    def setUp(self):
        # runs before every test case
        global jimid
        with sqlite3.connect(Account.dbpath) as conn:
            cur = conn.cursor()
            SQL = f"DELETE FROM {Account.tablename}"
            cur.execute(SQL)
            SQL = f"""INSERT INTO {Account.tablename}(first, last, username, password_hash, balance, email) 
            VALUES ("Jim", "Love", "JimmyLove", "Jim1966", 0, "jimmylove@gmail.com")"""
            cur.execute(SQL)
            jimid = cur.lastrowid

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
