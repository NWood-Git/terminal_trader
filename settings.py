import os

dirname = os.path.dirname(__file__)
DBPATH = os.path.join(dirname, "app", "data.db")  #removed ,"app" from middle
TESTDBPATH = os.path.join(dirname, "test", "_test.db")