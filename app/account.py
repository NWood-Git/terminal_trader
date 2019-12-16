from settings import DBPATH
from app import view
import sqlite3
import bcrypt
import requests
from credentials import PUBLICKEY
from app import position
from app.position import Position
from app import trade
from app.trade import Trade
import time
from time import ctime

class InsufficientFundsError(Exception):
    # create a new type of exception to check for with try & except
    pass

class InsufficientSharesError(Exception):
    pass

class NegativeQuantityError(Exception):
    pass

def get_quote(ticker):#gets full quote - f string important info
    REQUEST_URL = "https://cloud.iexapis.com/stable/stock/{ticker}/quote/?token={public_key}"
    GET_URL = REQUEST_URL.format(ticker=ticker, public_key=PUBLICKEY)
    response = requests.get(GET_URL)
    if response.status_code != 200:
        raise ConnectionError
    # elif response.status_code = 404:
    #     raise TickerNotFoundError
    data = response.json()
    return data
# print(account.get_quote("f"))
# x = account.get_quote("f")
# print(x['latestPrice'])



class Account:
    tablename = 'accounts'
    dbpath = DBPATH###should it be self.dbpath in the in the below functions? - Yes
    PUBLICKEY = PUBLICKEY

    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk')
        self.first = kwargs.get('first')
        self.last = kwargs.get('last')
        self.username = kwargs.get('username')
        self.password_hash = kwargs.get('password_hash')
        self.balance = kwargs.get('balance',0.0)
        self.email = kwargs.get('email')
        self.admin = kwargs.get('admin',0)#New
    
    def __repr__(self):
        return f"<{type(self).__name__} {self.__dict__}>"

    def save(self):
        ''' if the class instance is already in the database
            it will call the update function to update it
            otherwise it will create the insance in the database'''
        if self.pk is None:
            self.insert()
        else:
            self.update()
    
    def insert(self):
        '''this inserts the class instance into the database'''
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            if self.username == "admin":#NEW
                self.admin = 1#NEW
            SQL = f"""INSERT INTO {self.tablename}(first, last, username, password_hash, balance, email, admin)
                    VALUES(:first, :last, :username, :password_hash, :balance, :email, :admin);"""
            cur.execute(SQL, {'first':self.first, 'last':self.last, 'username':self.username, 'password_hash':self.password_hash, 'balance':self.balance, 'email':self.email, 'admin':self.admin})
            self.pk = cur.lastrowid

    def update(self):
        """updates an already exisitng pk in the database"""
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = f"""UPDATE {self.tablename} SET first=:first, last=:last, username=:username, 
            password_hash=:password_hash, balance=:balance, email=:email, admin=:admin WHERE pk =:pk;"""
            cur.execute(SQL, {'pk':self.pk, 'first':self.first, 'last':self.last, 'username':self.username, 'password_hash':self.password_hash, 'balance':self.balance, 'email':self.email, 'admin':self.admin})

    def delete(self):
        """deleting a user's row from the database"""
        with sqlite3.connect(self.dbpath) as conn:
            cur = connection.cursor
            SQl = f"DELETE FROM {self.tablename} WHERE pk=:pk;"
            cur.execute(SQL, {"pk" : self.pk})
            self.pk = None


    @classmethod #did in class 
    def all(cls):
        SQL = f"SELECT * FROM {cls.tablename};" # SELECT statements will be classmethods

        with sqlite3.connect(cls.dbpath) as conn:
            # make fetch method calls return a dictionary-like object for rows
            # with keys = column names
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            #execute SELECT * FROM accounts;
            cur.execute(SQL)
            #get a list of all rows as dictionary-like Row objects
            rows = cur.fetchall()
            #for each of these rows, call the class, Account(**row) where **row expands
            #a row from the select query into paramater to __init__
            result = [cls(**row) for row in rows]
            return result

            

    @classmethod
    def from_pk(cls,pk):
        SQL = f"SELECT * FROM {cls.tablename} WHERE pk=:pk;"
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, {"pk":pk})
            row = cur.fetchone()
            if row is None:
                return None
            result = cls(**row)
            return result #result is returning a class instance
    
    def set_password(self, password):
        #use code from John to create with bcrypt / hashing ## need to test
        self.password_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        # self.save()
    
    # def verify_password(self, password): #done in class 12/9 
    #     return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash)#pulling a bytes object from DB
        
    @classmethod
    def from_username(cls,username):
        SQL = f"SELECT * FROM {cls.tablename} WHERE username=:username;"
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(SQL, {"username":username})
            row = cur.fetchone()
            if row is None:
                return None
            result = cls(**row)
            return result #result is returning a class instance
    
    @classmethod
    def login_attempt(cls, username, password):#password from user input
        acct = cls.from_username(username)
        if acct == None:
            return None
        else:
            check = acct.verify_password(password)
            if check is True:
                # print(acct.first)
                # print(type(acct))
                return acct
            else:
                return None
    
    def trade(self, ticker, quantity, price = None):
        quantity = int(quantity)
        quote = get_quote(ticker)
        if price == None:
            if quote['iexAskPrice'] != 0 and quote['iexAskPrice'] is  not None: ##added the or
                price = float(quote['iexAskPrice'])
            else:
                price= float(quote['latestPrice'])
        else: #price != None
            price = price
        market_value = price * quantity
        position = Position.from_account_and_ticker(self.pk, ticker)
        if market_value > 0:#BUY
            if self.balance < market_value:
                # return None
                raise InsufficientFundsError
            else:
                self.balance -= market_value
                self.save()
        else:#SELL so market_value < 0
            if position.total_quantity < (quantity * -1):#
                raise InsufficientSharesError
                # return None
            else:#where we have more shares than whe are selling 
                self.balance += market_value * -1
                self.save()
        position.total_quantity += quantity #position.quantity is total quantity
        position.save()
        # now, create a new Trade object
        trade = Trade(ticker=ticker, account_pk=self.pk, quantity=quantity, price=price)
        trade.save()
        return abs(market_value) #had return True


                
    def withdraw(self, amount):
        if not isinstance(amount,float):
            raise TypeError("Withdrawal amount must be a float.")
        if amount < 0.0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError("""Sorry, you have insufficient funds
                                        to perform this transaction.""")
        self.balance -= amount
        self.save()
    
    def deposit(self, amount):
        if not isinstance(amount,float):
            raise TypeError("The deposit amount must be a float.")
        if amount < 0.0:
            raise ValueError("The deposit amount must be positive")
        self.balance += amount
        self.save()

    def show_holdings_by_account(self):
        positions = Position.all_from_account(self.pk)
        if positions == []:
            print("\nYou do not have any positions.\n")
        else:
            stock_mv = []
            for position in positions:
                if position.total_quantity > 0:
                    print(f"""Ticker: {position.ticker.upper()}     Quantity: {position.total_quantity}     Market Value: ${position.value()}""")
                    stock_mv.append(position.value())
            print(f"\nTotal Market Value of Stock Holdings: ${sum(stock_mv)}")
            print(f"Cash Balance in Account: ${round(self.balance,2)}")
            print(f"Total Value of Your Portfolio: ${(sum(stock_mv)+round(self.balance,2))}\n\n")

    def show_trades_by_account(self):
        trades = Trade.from_account_pk(self.pk)
        if trades == []:
            print("\nYou have not made any trades yet.\n")
        else:
            for trade in trades:
                if trade.quantity < 0:
                    trade_type = "Sell"
                else:
                    trade_type = "Buy"
                print(f"Trade Type: {trade_type},  Ticker: {trade.ticker.upper()},  Quantity: {abs(trade.quantity)},  Price: ${trade.price},  Market Value: ${round(abs(trade.price*trade.quantity),2)},  Created At: {ctime(trade.created_at)}")
            print("\n")

    def show_trades_by_account_and_ticker(self,ticker):
        trades = Trade.from_account_and_ticker(self.pk,ticker)
        if trades == []:
            view.never_traded_invalid()#TODO: run it through the quote function and include try/except for invalid ticker
        else:
            for trade in trades:
                if trade.quantity < 0:
                    trade_type = "Sell"
                else:
                    trade_type = "Buy"
                print(f"Trade Type: {trade_type},  Ticker: {trade.ticker.upper()},  Quantity: {abs(trade.quantity)},  Price: ${trade.price},  Market Value: ${round(abs(trade.price*trade.quantity), 2)},  Created At: {ctime(trade.created_at)}")
        print("\n")

    def leaderboard_stats_by_acct(self, account_pk, username):
        positions = Position.all_from_account(account_pk)
        stock_mv = []
        for x in positions:
            if x.total_quantity > 0:
                stock_mv.append(x.value())
        print(f"Account pk: {account_pk}, Username: {username}, Total Stock Value: ${sum(stock_mv)}, Cash Balance: ${round(self.balance,2)}, Total Portfolio Value: ${(sum(stock_mv)+round(self.balance,2))}")



# Below 3 lines for classmethod from username just showing how it works
# x= Account.from_username("JBau24")
# print(x)
# print(x.balance)


   # def buy(self, ticker, quantity):
    #     quantity = int(quantity)
    #     quote = self.get_quote(ticker,PUBLICKEY)
    #     if quote['iexAskPrice'] != 0:
    #         price = float(quote['iexAskPrice'])
    #     else:
    #         price= float(quote['latestPrice'])
    #     market_value = price * quantity
    #     if self.balance < market_value:
    #         return None
    #     else:
    #         # now, get the position object for this account and this ticker ####REMOVE AVG_PRICE
    #         position = Position.from_account_and_ticker(self.pk, ticker)
    #         # then position.quantity += quantity
    #         new_avg_px = ((position.total_quantity*position.avg_price) + (quantity*price)) /(position.total_quantity+quantity)#new line
    #         position.avg_price = new_avg_px
    #         position.total_quantity += quantity #position.quantity is total quantity
    #         # now, create a new Trade object
    #         trade = Trade(ticker=ticker, account_pk=self.pk, quantity=quantity, price=price)
    #         self.balance -= market_value
    #         position.save()
    #         trade.save()
    #         self.save()
    #         return True   