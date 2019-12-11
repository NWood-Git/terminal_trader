###This Group of Functions if for the inital login menu
def print_login_menu():
    '''this is the first menu the user sees when using terminal trader'''
    
    print("""Welcome to Terminal Trader
    Please choose one of the following options:

    1. Create a new account
    2. Log In
    3. Exit 
    """)

def login_prompt():
    return input("Your choice: ")

def bad_login_input():
    print("Input not recognized. Please select 1,2, or 3. \n")

def goodbye():
    print("    Goodbye!\n")

def user_login_attempt():
    print("Please enter your credentials. ")
    login_username = input("Username: ")
    login_password = input("Password: ")
    return (login_username, login_password)


#### This group of view functions are for the create_account function in main ####

def intro_create_acc():
    print("""Hello, thank you for creating an account with us!
    Please follow the instructions below:""")

def input_first():
    first = input("What is your first name? ")
    return first.strip().title()

def input_last():
    last = input("What is your last name? ")
    return last.strip().title()

def input_username():
    username = input("Please pick an user name: ")
    return username.strip()

def input_password():
    while True:
        password = input("Please enter your password: ")
        confirm_pw = input("Please re-enter your password for confirmation: ")
        if password == confirm_pw:
            return password.strip()
            break
        else:
            print("Your passwords didn't match, please try again.")

def input_email():
    while True:        
        email = input("Please input your email: ")
        confirm_email = input("Please re-enter your email for confirmation: ")
        if email == confirm_email:
            return email.strip()
            break
        else:
            print("Your emails didn't match, please try again.")

###This group of Functions is related to the main menu####
def print_main_menu(user):
    print(f"""Hello, {user.first} {user.last}

    Please select one of the below options:
    1 Check Balance                                                       
    2 Withdraw Funds                                                           
    3 Deposit Funds
    4 Trading Menu
    5 Exit to Menu
""")

def main_prompt():
    return input("Your choice: ")

def bad_menu_input():
    print("Your input is not valid. Please select 1,2,3,4, or 5. \n")

def show_balance(user):
    print(f"Your balance is ${user.balance}")

def withdrawal_amount():#could get rid of limits and do unittest
    while True:
        amount = input("How much would you like to withdraw?: ")
        if amount.isnumeric() is True:
            amount = float(amount)
            return amount
        else:
            print("Input not valid: please enter a numeric value.")

def not_positive():
    print("""Sorry, you can't withdraw a negative number. 
        The amount you enter needs to be positive!""")

def insufficient_funds():
    print("Sorry you have insufficient funds to perform for this transaction.")

def post_withdrawal(amount, balance):
    print(f"You have withdrawn ${amount} and now your balance is ${balance}.")

def deposit_amount():#could get rid of limits and do unittest
        while True:
            amount = input("How much would you like to deposit?: ")
            if amount.isnumeric() is True:
                amount = float(amount)
                return amount
            else:
                print("Input not valid: please enter a numeric value.")

def post_deposit(amount, balance):
    print(f"You have deposited ${amount} and now your balance is ${balance}.")

#######This group of fucntions relates to the Trading Menu########
def print_trading_menu(user):
    print(f"""Hello, {user.first} {user.last}. Please see the Trading Menu:

    Please select one of the below options:
    1 Get Quote                                                       
    2 Buy Shares                                                           
    3 Sell Shares
    4 See Positions
    5 Exit to Previous Menu
""")

def trading_menu_prompt():
    return input("Your choice: ")

def ticker_prompt():
    ticker = input("Please input the ticker of the stock whose quote you want to see: ")
    return ticker.lower()

def connection_error():
    print("Error: either your ticker is invalid or there are connection issues.\n")