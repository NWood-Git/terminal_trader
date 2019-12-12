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
        self.total_quantity = kwargs.get("total_quantity")
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
            SQL = f""" INSERT INTO {self.tablename}(account_pk, total_quantity, ticker, avg_price)
                    VALUES(:account_pk, :total_quantity, :ticker, :avg_price)"""
            cur.execute(SQL,{'account_pk':self.account_pk, 'total_quantity':self.total_quantity,'ticker':self.ticker, "avg_price":self.avg_price})
            self.pk = cur.lastrowid

    def update(self):
        ###TODO UPDATE total quantity and average price
        """Updates an already existing pk in the database"""
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = f"""UPDATE {self.tablename} SET account_pk=:account_pk, 
            total_quantity=:total_quantity, ticker=:ticker, avg_price=:avg_price"""
            cur.execute(SQL,{'pk':self.pk, 'account_pk':self.account_pk, 'total_quantity':self.total_quantity,'ticker':self.ticker, 'avg_price':self.avg_price})
        
    @classmethod
    def all(cls):#Tested w/ manual - worked
        SQL = f"SELECT * FROM {cls.tablename};"
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL)
            rows = cur.fetchall()
            result = [cls(**row) for row in rows]
            return result #result is a list of class instances

    @classmethod
    def from_pk(cls,pk):#Tested w/ manual - worked
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

    @classmethod#Tested w/ manual - worked
    def from_account_and_ticker(cls, account_pk, ticker):#how to feed in from account
        '''return position object where account_pk = account.pk and ticker = ticker'''
        SQL = f"SELECT * FROM {cls.tablename} WHERE account_pk=:account_pk AND ticker=:ticker"
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, {'account_pk':account_pk, 'ticker':ticker })
            row = cur.fetchone()
            if row is None:
                new_pos = Position(account_pk = account_pk, total_quantity = 0, ticker = ticker, avg_price = 0)
                new_pos.save() #should this be here?
                return new_pos #CA-instead of None return a new Position with zero shares, Position(amount=0, account_id=account_pk, ticker=ticker)
            result = cls(**row)
            return result #result is a class instance



    # def value(self,ticker, public_key, param): ###not working### Test after creating instance
    #     px = account.get_specific_quote(ticker, public_key, param)
    #     total_quantity = 100 #self.total_quantity
    #     market_value = px * total_quantity
    #     print(market_value)



# ###old more complicated way to save - do not use

#     def save(self, ticker, total_quantity, price, account_pk):
#         """if the postion doesn't exist we call the insert function
#         if it does exist we call the update function
#         to insert or udpate the position in the database"""
#         with sqlite3.connect dbpath as conn:
#             conn.row_factory = sqlite3.Row
#             cur = conn.cursor()
#             SQL = f"""SELECT * FROM {self.tablename} WHERE ticker=:ticker AND account_pk=:account_pk;"""
#             cur.execute(SQL, {"ticker"=:ticker, "account_pk":=account_pk})
#             row = cur.fetchone()
#             total_quantity = row['total_quantity']
#             avg_price - row['avg_price']
#             if row is None:
#                 self.insert()
#             else:
#                 self.update()
        
#     def insert(self, ticker, quantity, price, account_pk):#works - with manual instance creation
#         #? account_pk should it pull from Account class
#         # how does the calculated value avg price work in a class
#         """This fucntion inserts a class instance into the database"""
#         with sqlite3.connect(self.dbpath) as conn:
#             cur = conn.cursor()
#             SQL = f""" INSERT INTO {self.tablename}(account_pk, total_quantity, ticker, avg_price)
#                     VALUES(:account_pk, :total_quantity, :ticker, :avg_price);"""
#             cur.execute(SQL,{'account_pk':account_pk, 'total_quantity':quantity,'ticker':ticker, "avg_price":price})
#             self.pk = cur.lastrowid

#     def update(self,ticker, total_quantity, quantity, avg_price, price, account_pk):
#         #not tested
#         #same questions as above
#         """Updates an already existing pk in the database"""
#         with sqlite3.connect(self.dbpath) as conn:
#             cur = conn.cursor()
#             SQL = f"""UPDATE {self.tablename} SET account_pk=:account_pk, 
#             total_quantity=:total_quantity, ticker=:ticker, avg_price=:avg_price;"""
#             new_total_quantity = total_quantity + quantity
#             new_tot_mv = (total_quantity * avg_price) + (quantity * price)
#             new_avg_price = new_tot_mv / (total_quantity + quantity)
#             cur.execute(SQL,{'pk':self.pk, 'account_pk':self.account_pk, 'total_quantity':new_total_quantity,'ticker':self.ticker, 'avg_price':new_avg_price})
