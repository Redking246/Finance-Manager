import sqlite3
import os
import datetime


print("""
██████╗  █████╗ ███╗   ██╗██╗  ██╗
██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝
██████╔╝███████║██╔██╗ ██║█████╔╝
██╔══██╗██╔══██║██║╚██╗██║██╔═██╗
██████╔╝██║  ██║██║ ╚████║██║  ██╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝

        TERMINAL BANKING SYSTEM
========================================
Type 'help' to see available commands
""")

#Creates the database
con = sqlite3.connect("bank.db")
cur = con.cursor()
#Adds the tables to the database
cur.execute("CREATE TABLE IF NOT EXISTS account(name, balance, currency)")
cur.execute("CREATE TABLE IF NOT EXISTS transactions(date, details, amount, incomeflag)")

#Asks the user for account details eg. Name,starting balance and currency
cur.execute("SELECT name FROM account")
result = cur.fetchall()
currency_list = {"EUR": "€","USD": "$","GBP": "£","JPY": "¥"}
if result == []:
    name = input("Name for account:")
    balance_prompt = "Starting balance for account:"
    while True:
        try:
            balance = round(float(input(balance_prompt)), 2)
            break
        except ValueError:
                balance_prompt = "Please type a valid number:"
    currency = input("Type either EUR, USD, GBP, JPY:").upper()
    while True:
        if currency not in currency_list:
           currency = input("Type one of the currencies:").upper()
        else:
            break 
    cur.execute("INSERT INTO account VALUES(?, ?, ?)", (name, balance, currency,))
    con.commit()


#Tuple that contains the list of commands used when the user types help
help_list = (
"balance: Displays the balance of the current account in use",
"new entry: Adds a new entry to either income or expenditure",
"exit: Closes the program",
"help: Displays this list" ,
"reset: Resets all accounts",
"show transactions: Shows a table of transactions",
)


#Main loop
while True:
    cur.execute("SELECT name, balance, currency FROM account")
    account = cur.fetchall()
    command = input(f"Hello, {account[0][0]} ❯ ").lower()
    if command == "balance":
        print(f"Your balance is: {currency_list[account[0][2]]}{account[0][1]}")
    #creates a new 
    elif command == "new entry":
        incomeflag = input("Income or Expenditure:")
        while True:
            if incomeflag not in ("income", "expenditure"):
                incomeflag = input("Please write either income or expenditure:")
            else:
                break
        date_prompt = "Date in YYYY-MM-DD:"
        while True:
            date = input(date_prompt)
            try:
                datetime.date.fromisoformat(date)
                break
            except:
               date_prompt = "Please type a valid date:"
        details = input("Details:")
        amount_prompt = "Amount:"
        while True:
            try:
                amount = round(float(input(amount_prompt)), 2)
                break
            except ValueError:
                amount_prompt = "Please type a number:"
        cur.execute("INSERT INTO transactions VALUES(?, ?, ?, ?)", (date, details, amount, incomeflag))
        con.commit() 
        if incomeflag == "income":
            cur.execute("UPDATE account SET balance = balance + ?", (amount,))
            con.commit()
        elif incomeflag == "expenditure":
            cur.execute("UPDATE account SET balance = balance - ?", (amount,))
            con.commit()

    elif command == "exit":
        break
    elif command == "help":
        for help in help_list:
            print(help)
    elif command == "show transactions":
        cur.execute("SELECT date, details, amount, incomeflag FROM transactions")
        rows = cur.fetchall()
        if not rows:
            print("No transactions found.")
        else:
            headers = ["Date", "Details", "Amount", "Type"]

            
            col_widths = [len(h) for h in headers]
            for row in rows:
                for i, value in enumerate(row):
                    col_widths[i] = max(col_widths[i], len(str(value)))
            line = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
            print(line)          
            header_row = "| " + " | ".join(headers[i].ljust(col_widths[i]) for i in range(len(headers))) + " |"
            print(header_row)
            print(line)
            for row in rows:
                row_text = "| " + " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row))) + " |"
                print(row_text)
            print(line)

    elif command == "reset":
        reset = input("Are you sure you want to reset?:")
        if reset == "yes":
            os.remove("bank.db")
            print("Account reset successfully")
            break           
    else:
        print("Command not found, type 'help' for list of commands")