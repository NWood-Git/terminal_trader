from app import account
from app import position
from app.account import Account
from app.position import Position
from app.trade import Trade
from app import view
import settings
import bcrypt
from credentials import PUBLICKEY

#to reactivate virtual enviroment: source venv/bin/activate
def run():
    while True:
        user_account = login_menu()  # returns the logged in user or None for quit
        if user_account == None:  # login menu returns None if 'quit' is selected
            view.goodbye()
            break
        main_menu(user_account) #removed arguement user_account # when the user exits the main menu they will go back to login

def login_menu():#removed user as arg
    """This is the first menu that the user sees"""
    while True:
        view.print_login_menu()
        choice = view.login_prompt().strip()
        if choice not in ("1", "2", "3"):
            view.bad_login_input()
        elif choice == "3":
            return None #returns none to exit function from run
        elif choice == "1":#choice 1 = create account #NW added the below code in choice 1
            """calls create_account() function """
            create_account()
            pass #needed?
        elif choice == "2":
            account = login()
            if attempt is True:## needs to be fixed does return true need to get to main menu
                # print('yay')
                break #temp
            else:
                pass

def main_menu():
    'THIS IS THE MAIN MENU'


def create_account():
    view.intro_create_acc()
    first = view.input_first()
    last = view.input_last()
    username = view.input_username()
    password = view.input_password() #this is the start of what will become the password hash
    balance = 0
    email = view.input_email()
    new_account = Account(first=first, last=last, username=username, balance=balance, email=email) #password_hash=password_hash - not used b/c save in set pw fucntion
    new_account.set_password(password) #creates the password has which is missing in the above line
    new_account.save()#save function to put the new account into the sql db

def login(): 
    username, password = view.user_login_attempt()
    check = Account.login_attempt(username, password)
    if True:
        return True
    else:
        return None

            


# create_account() #to test
# print(login())#njet247 , password #to test
# run()

# print(account.get_quote("f",PUBLICKEY))
# x = account.get_quote("f",PUBLICKEY)
# print(x['latestPrice'])
# position.value("f","pk_6121dd71b3dd479a9d12851b3520849b", "latestPrice") #test after creating an intance of position