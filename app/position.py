from settings import DBPATH
import sqlite3
from app import account


class Position:
    tablename = "positions"
    dbpath = DBPATH

    def __init__(self, **kwargs):
        self.pk = kwargs.get("pk")
        self.account_pk = kwargs("account_pk")
        self.quantity = kwargs.get("quantity")
        self.ticker = kwargs.get("ticker")
        self.avg_price = kwargs.get("avg_price")
        

    def __repr__(self):
        return f"<{type(self).__name__} {self.__dict__}>"
    
    def save():
        """if the postion doesn't exist we call the insert function
        if it does exist we call the update function
        to insert or udpate the position in the database"""
        if self.pk is None:
            self.insert()
        else:
            self.update()
    
    def insert(self):
        # not tested - ? account_pk should it pull from Account class
        # how does the calculated value avg price work in a class
        """This fucntion inserts a class instance into the database"""
        with sqlite3.connect(dbpath) as conn:
            cur = conn.cursor()
            SQL = f""" INSERT INTO {self.tablename}(account_pk, quantity, ticker, avg_price)
                    VALUES(:account_pk, :quantity, :ticker, :avg_price)"""
            cur.execute(SQL,{'account_pk':self.account_pk, 'quantity':self.quantity,'ticker':self.ticker, "avg_price":self.avg_price})
            self.pk = cur.lastrowid

    def update(self):
        #not tested
        #same questions as above
        """Updates an already existing pk in the database"""
        with sqlite3.connect(dbpath) as conn:
            cur = conn.cursor()
            SQL = f"""UPDATE {self.tablename} SET account_pk=:account_pk, 
            quantity=:quantity, ticker=:ticker, avg_price=:avg_price"""
            cur.execute(SQL,{'pk':self.pk, 'account_pk':self.account_pk, 'quantity':self.quantity,'ticker':self.ticker, 'avg_price':self.avg_price})

    # def value(self,ticker, public_key, param): ###not working### Test after creating instance
    #     px = account.get_specific_quote(ticker, public_key, param)
    #     quantity = 100 #self.quantity
    #     market_value = px * quantity
    #     print(market_value)
    
    ##ADD from ID fucnt

    @classmethod
    def from_account_and_ticker(cls, account, ticker):
        pass
        #return position object where account_pk = account.pk and ticker = ticker


# new_pos_1 = 