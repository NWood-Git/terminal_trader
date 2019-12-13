from settings import DBPATH
import sqlite3
from app import account
from credentials import PUBLICKEY
import time

class Trade:
    tablename = "trades"
    dbpath = DBPATH
    PUBLICKEY = PUBLICKEY

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.account_pk = kwargs.get("account_pk")
        self.ticker = kwargs.get("ticker")
        self.quantity = kwargs.get("quantity")
        self.price = kwargs.get("price")
        self.created_at = kwargs.get("created_at", time.time())

    def __repr__(self):
        return f"<{type(self).__name__} {self.__dict__}>"
    
    def save(self):
        """if the trade is in the trades database update is called
        otherwise insert is called to create a new position in the database"""
        self.insert()
        # if self.pk is None:
        #     self.insert()
        # else:
        #     self.update()
    
    def insert(self):
        """this inserts the new trades class instance into the database"""
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = f"""INSERT INTO {self.tablename}(account_pk, ticker, quantity, price, created_at)
                    VALUES(:account_pk, :ticker, :quantity, :price, :created_at)"""
            cur.execute(SQL, {'account_pk':self.account_pk,'ticker':self.ticker, 'quantity': self.quantity, 'price':self.price,"created_at":self.created_at})
            # cur.execute(SQL, self.__dict__)#may work
            self.pk = cur.lastrowid
            #is created_at in the right spot?

    # def update(self):#NOT NEEDED FOR TRADES?
    #     """updates an already existing pk in the database"""
    #     with sqlite3.connect(self.dbpath) as conn:
    #         cur = conn.cursor()
    #         SQL = f"""UPDATE {self.tablename} SET account_pk=:account_pk, 
    #             ticker=:ticker, quantity=:quantity WHERE pk=:pk;"""
    #         cur.execute(SQL,{'pk':self.pk, 'account_pk':self.account_pk, 'ticker':self.ticker, 'quantity':self.quantity, 'created_at':self.created_at})

    @classmethod
    def all(cls):
        SQL = f"SELECT * FROM {cls.tablename};"
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = con.cursor()
            rows = cur.fetchall()
            result = [cls(**row) for row in rows]
            return result #returns a list of class instances
    
    @classmethod
    def from_pk(cls,pk):
        SQL = f"SELECT * FROM {cls.tablename} WHERE pk:=pk;"
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL,{'pk':pk})
            row = cur.fetchone()
            if row is None:
                return None
            result = cls(**row)
            return result #result is a class instance

    @classmethod
    def from_account_pk(cls, account_pk):
        SQL = f"SELECT * FROM {cls.tablename} WHERE account_pk=:account_pk;"
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, {'account_pk': account_pk})
            rows = cur.fetchall()
            result = [cls(**row) for row in rows] #returns a list of class instances
    
    @classmethod
    def from_account_and_ticker(cls, account_pk,ticker):
        """return trades with a specific account_pk and ticker combination"""
        SQL = f"""SELECT * FROM {cls.tablename} WHERE account_pk=:account_pk
                AND ticker=:ticker;"""
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur= conn.cursor()
            cur.execute(SQL, {'account_pk':account_pk, 'ticker':ticker})
            rows = cur.fetchall()
            result = [cls(**row) for row in rows] #returns a list of class instances
