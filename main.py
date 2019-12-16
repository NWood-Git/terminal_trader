from app import account
from app import position
from app.account import Account, InsufficientFundsError, InsufficientSharesError
from app.position import Position
from app.trade import Trade
from app import view
import settings
import bcrypt
import requests
from credentials import PUBLICKEY
from time import ctime

#to reactivate virtual enviroment: source venv/bin/activate
#to leave virtual enviroment: deactivate

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
            try:
                create_account()
            except view.UsernameUnavailableError:
                view.invalid_username()
            pass #needed?
        elif choice == "2":
            account = login()
            if account:## needs to be fixed does return true need to get to main menu
                return account# print('yay')
            else:
                pass

def main_menu(user):
    while True:
        if user.username == 'admin':
            view.print_admin_menu(user)
            choice = view.main_prompt()
        else:    
            view.print_main_menu(user)
            choice = view.main_prompt()
        if choice  == "1":
            view.show_balance(user)#Check Balance
            pass
        elif choice == "2":#Withdraw Funds
            amount = view.withdrawal_amount()
            try:
                user.withdraw(amount)#func is in account.py
                view.post_withdrawal(amount, user.balance)
            except ValueError:
                view.not_positive()
            except account.InsufficientFundsError:
                view.insufficient_funds()
        elif choice == "3":#Deposit Funds
            amount = view.deposit_amount()
            try:
                user.deposit(amount)
                view.post_deposit(amount, user.balance)
            except ValueError:
                view.not_positive()
        elif choice == "4":#Trading Menu
            trading_menu(user)
        elif choice == "5":#Sign Out #exits to first login menu
            break
        elif choice == "6":#Admin - Leaderboard
            if user.username == 'admin':
                admin_leaderboard()
            else:
                view.bad_menu_input()
        elif choice == "7":
            if user.username == 'admin':
                print("You can see choice 7 because you are an admin.")
            else:
                view.bad_menu_input()
        else:#loops back
            view.bad_menu_input()
            continue
        

def trading_menu(user):
    while True:
        view.print_trading_menu(user)
        choice = view.trading_menu_prompt()
        if choice == "1":#GetQuote
            ticker = view.ticker_prompt()
            try:
                quote = account.get_quote(ticker)
                # print(quote) #shows whole quote as json dictionary
                print(f"""
                Company Name: {quote['companyName']}
                Symbol: {quote['symbol']} 
                Latest Price: {quote['latestPrice']}
                IEX Bid Price: {quote['iexBidPrice']}
                IEX Ask Price: {quote['iexAskPrice']}
                High: {quote['high']}
                Low: {quote['low']}
                52 Week High: {quote['week52High']}
                52 Week Low: {quote['week52Low']}
                PE Ratio {quote['peRatio']}\n\n""")
            except ConnectionError:
                view.connection_error()
        elif choice == "2":#Buy Shares NOT COMPLETE
            view.buy_intro()
            ticker = view.ticker_prompt()
            quantity = view.quantity()
            try:
                quantity = int(quantity)
                if quantity < 0:
                    view.negative_quantity_error()#TODO: fix this so it doesn't send you back to trading menu
                elif quantity == 0:
                    view.zero_quantity_error()
                else:
                    try:
                        market_value = user.trade(ticker, quantity)
                        view.sucessful_buy_trade(ticker, quantity, market_value)
                    except InsufficientFundsError:
                        view.insufficient_funds()
                    except ConnectionError:
                        view.connection_error()
            except ValueError:
                view.not_number_error()
        elif choice =="3":#Sell Shares
            view.sell_intro()
            ticker = view.ticker_prompt()
            quantity = view.quantity()
            try:
                quantity = int(quantity)
                if quantity < 0:
                    view.negative_quantity_error()#TODO: fix this so it doesn't send you back to trading menu
                elif quantity == 0:
                    view.zero_quantity_error()
                else:
                    quantity = quantity * -1
                    try:
                        market_value = user.trade(ticker, quantity)
                        view.sucessful_sell_trade(ticker, quantity, market_value)
                    except InsufficientSharesError:
                        view.insufficient_shares()
                    except ConnectionError:
                        view.connection_error()
            except ValueError:
                view.not_number_error()
            # except account.NegativeQuantityError:
            #     view.negative_quantity_error()
        elif choice == "4":#See Holdings
            user.show_holdings_by_account()
        elif choice == "5":#Show Trade History
            while True:
                selection = view.trade_history_prompt()
                if selection.lower() == "quit":
                    break
                elif selection.lower() == "total":
                    user.show_trades_by_account()
                    break
                else:
                    user.show_trades_by_account_and_ticker(selection)
                    break
        elif choice == "6":#Exit to Menu
            break
        else:
            view.bad_menu_input()


def create_account():
    view.intro_create_acc()
    first = view.input_first()
    last = view.input_last()
    username = view.input_username()
    password = view.input_password() #this is the start of what will become the password hash
    balance = 0
    email = view.input_email()
    new_account = Account(first=first, last=last, username=username, balance=balance, email=email)
    #password_hash=password_hash - not used b/c save in set pw fucntion
    new_account.set_password(password) #creates the password has which is missing in the above line
    if Account.from_username(username) is None:
        new_account.save()#save function to put the new account into the sql db
    else:
        raise view.UsernameUnavailableError

def login(): 
    username, password = view.user_login_attempt()
    loaded_acct = Account.login_attempt(username, password)
    if loaded_acct:
        return loaded_acct #True
    else:
        view.invalid_credentials()
        return None

def admin_leaderboard():
    print('Terminal Trader Leaderboard\n')
    accounts = Account.all()
    account_username_pk_list = []
    for account in accounts:
        account_username_pk_list.append([account, account.pk, account.username])
    for item in account_username_pk_list:
        Account.leaderboard_stats_by_acct(item[0], item[1], item[2])




# def show_holdings_by_account(user):
#     positions = Position.all_from_account(user.pk)
#     stock_mv = []
#     for position in positions:
#         if position.total_quantity > 0:
#             print(f"""Ticker: {position.ticker.upper()}     Quantity: {position.total_quantity}     Market Value: ${position.value()}""")
#             stock_mv.append(position.value())
#     print(f"\nTotal Market Value of Stock Holdings: ${sum(stock_mv)}")
#     print(f"Cash Balance in Account: ${round(user.balance,2)}")
#     print(f"Total Value of Your Portfolio: {(sum(stock_mv)+round(user.balance,2))}\n\n")

# def show_trades_by_account(user):
#     trades = Trade.from_account_pk(user.pk)
#     for trade in trades:
#         if trade.quantity < 0:
#             trade_type = "Sell"
#         else:
#             trade_type = "Buy"
#         print(f"Trade Type: {trade_type},  Ticker: {trade.ticker.upper()},  Quantity: {abs(trade.quantity)},  Price: ${trade.price},  Market Value: ${round(abs(trade.price*trade.quantity),2)},  Created At: {ctime(trade.created_at)}")
#     print("\n")

# def show_trades_by_account_and_ticker(user,ticker):
#     trades = Trade.from_account_and_ticker(user.pk,ticker)
#     if trades == []:
#         view.never_traded_invalid()#TODO: run it through the quote function and include try/except for invalid ticker
#     else:
#         for trade in trades:
#             if trade.quantity < 0:
#                 trade_type = "Sell"
#             else:
#                 trade_type = "Buy"
#             print(f"Trade Type: {trade_type},  Ticker: {trade.ticker.upper()},  Quantity: {abs(trade.quantity)},  Price: ${trade.price},  Market Value: ${round(abs(trade.price*trade.quantity), 2)},  Created At: {ctime(trade.created_at)}")
#     print("\n")

###############
run()
# create_account() #to test
# print(login())#njet247 , password #to test #MarSim password

# new_pos_1 = Position(account_pk=1, quantity=10, ticker="f", avg_price=100) #test done and in DB
# new_pos_1.save()
# x = Position.all()
# x = Position.from_pk(1)
# x = Position.from_account_and_ticker(1, "f")
# print(x)
