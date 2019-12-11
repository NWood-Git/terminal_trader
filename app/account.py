from settings import DBPATH
from app import view
import sqlite3
import bcrypt
import requests
from credentials import PUBLICKEY


class Account:
    tablename = 'accounts'
    dbpath = DBPATH###should it be self.dbpath in the in the below functions?
    PUBLICKEY = PUBLICKEY

    def __init__(self, **kwargs):
        self.pk = kwargs.get('pk')
        self.first = kwargs.get('first')
        self.last = kwargs.get('last')
        self.username = kwargs.get('username')
        self.password_hash = kwargs.get('password_hash')
        self.balance = kwargs.get('balance',0.0)
        self.email = kwargs.get('email')
    
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
            SQL = f"""INSERT INTO {self.tablename}(first, last, username, password_hash, balance, email)
                    VALUES(:first, :last, :username, :password_hash, :balance, :email)"""
            cur.execute(SQL, {'first':self.first, 'last':self.last, 'username':self.username, 'password_hash':self.password_hash, 'balance':self.balance, 'email':self.email})
            self.pk = cur.lastrowid

    def update(self):
        """updates an already exisitng pk in the database"""
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            SQL = f"""UPDATE {self.tablename} SET first=:first, last=:last, username=:username, 
            password_hash=:password_hash, balance=:balance, email=:email WHERE pk =:pk"""
            cur.execute(SQL, {'pk':self.pk, 'first':self.first, 'last':self.last, 'username':self.username, 'password_hash':self.password_hash, 'balance':self.balance, 'email':self.email})

    def delete(self):
        """deleting a user's row from the database"""
        with sqlite3.connect(self.dbpath) as conn:
            cur = connection.cursor
            SQl = f"DELETE FROM {self.tablename} WHERE pk=:ok;"
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
    
    @classmethod #NOT COMPLETE - does this belong here?
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
    
    def buy(self, ticker, amount):
        bal = self.balance
        
    class InsufficientFundsError(Exception):
        # create a new type of exception to check for with try & except
        pass

    def withdraw(self, amount):
        if not isinstance(amount,float):
            raise TypeError("Withdraw must be a float.")
        if amount < 0.0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError("""Sorry, you have insufficient funds
                                        to perform this transaction.""")
        self.balance -= amount
        self.save()

    




# Below 3 lines for classmethod from username just showing how it works
# x= Account.from_username("JBau24")
# print(x)
# print(x.balance)