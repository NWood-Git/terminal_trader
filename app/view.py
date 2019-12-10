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
    return input("Your choice:")

def bad_login_input():
    print("Input not recognized. Please select 1,2, or 3. \n")

def goodbye():
    print("    Goodbye!\n")
#########
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
############################################