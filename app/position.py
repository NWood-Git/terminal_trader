from settings import DBPATH
import sqlite3
from app import account
from credentials import PUBLICKEY


class Position:
    tablename = "positions"
    dbpath = DBPATH
    PUBLICKEY = PUBLICKEY

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.account_pk = kwargs.get("account_pk")
        self.quantity = kwargs.get("quantity")
        self.ticker = kwargs.get("ticker")
        self.avg_price = kwargs.get("avg_price")
        

    def __repr__(self):
        return f"<{type(self).__name__} {self.__dict__}>"
    
    def save(self):
        """if the postion doesn't exist we call the insert function
        if it does exist we call the update function
        to insert or udpate the position in the database"""
        if self.pk is None:
            self.insert()
        else:
            self.update()
    
    def insert(self):#works - with manual instance creation
        # not tested - ? account_pk should it pull from Account class
        # how does the calculated value avg price work in a class
        """This fucntion inserts a class instance into the database"""
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = f""" INSERT INTO {self.tablename}(account_pk, quantity, ticker, avg_price)
                    VALUES(:account_pk, :quantity, :ticker, :avg_price)"""
            cur.execute(SQL,{'account_pk':self.account_pk, 'quantity':self.quantity,'ticker':self.ticker, "avg_price":self.avg_price})
            self.pk = cur.lastrowid

    def update(self):
        #not tested
        #same questions as above
        """Updates an already existing pk in the database"""
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = f"""UPDATE {self.tablename} SET account_pk=:account_pk, 
            quantity=:quantity, ticker=:ticker, avg_price=:avg_price"""
            cur.execute(SQL,{'pk':self.pk, 'account_pk':self.account_pk, 'quantity':self.quantity,'ticker':self.ticker, 'avg_price':self.avg_price})


    @classmethod
    def all(cls):#NOT Tested
        SQL = f"SELECT * FROM {self.tablename};"
        with sqlite3.connect(self.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL)
            rows = cur.fetchall()
            result = [cls(**row) for row in rows]
            return result #result is a list of class instances

    @classmethod
    def from_pk(cls):#NOT TESTED
        SQL = f"SELECT * FROM {cls.tablename} WHERE pk=:pk;"
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, {'pk':pk})
            row = cur.fetchone()
            if row is None:
                return None
            result = cls(**row)
            return result #result is a class instance

    @classmethod#NOT TESTED
    def from_account_and_ticker(cls, account_pk, ticker):#how to feed in from account
        '''return position object where account_pk = account.pk and ticker = ticker'''
        SQL = f"SELECT * FROM {cls.tablename} WHERE account_pk=:account_pk AND ticker=:ticker"
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, {'account_pk':account_pk, 'ticker':ticker })
            row = cursor.fetchone()
            if row is None:
                return None
            result = cls(**row)
            return result #result is a class instance



    # def value(self,ticker, public_key, param): ###not working### Test after creating instance
    #     px = account.get_specific_quote(ticker, public_key, param)
    #     quantity = 100 #self.quantity
    #     market_value = px * quantity
    #     print(market_value)

