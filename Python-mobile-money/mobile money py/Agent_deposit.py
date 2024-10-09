import datetime
import json
import os

filename = "Mobile_database.json"
text_name = "mini_statement.txt"
#filename = "Gui_database.json"
#text_name = "Gui_statement.txt"
x = datetime.datetime.now()
account_database = {
}

agent_id = 254254
agent_pin = 1212
agent_name = "Elianto"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def check_account_max():
    while True:
        amount = get_integer_input("Enter amount to deposit: ")
        with open(filename, "r") as file:
            database = json.load(file)
            accbal = database.get("balance")
        maxm = amount + accbal
        if maxm > 500000:
            print("Maximum amount for account is ksh 500,000")
            print("Try a lower amount")

        elif maxm < 500000:
            return amount


def store_transaction(transaction):
    with open(text_name, "a") as file:
        file.write(str(transaction) + '\n')


def get_integer_input(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input.Please enter an integer.")


def check_mobile_database():

    if os.path.exists(filename):
        if os.path.getsize(filename) == 0:
            with open(text_name,"w") as file:
                pass

            create_account(filename)

        else:
            print("An account exits!!")
            quit()

    else:
        create_account(filename)


def create_account(filename):
    x = datetime.datetime.now()
    g = 0
    p = 0
    a = 0
    f = 0
    print("To create an account enter the following")
    while g < 2:
        while f == 0:
            idn = get_integer_input("Enter customers ID number: ")
            if len(str(idn)) == 8:
                f = 1
            else:
                print("ID number should consist of 8 digits!!")

        name = input("Enter customers full names(AT LEAST TWO NAMES): ")
        name_parts = name.split()

        if len(name_parts) >= 2:
            g = 2
        else:
            print("Names should at least be two!!")
    print("Format eg 0712345678")
    while True:
        phone_number = get_integer_input("Enter phone number: ")
        if len(str(phone_number)) == 9:
            break
        else:
            print("it should be 10 digits")

    while p != 1:
        pin = input("Please enter a 4-digit PIN: ")

        if pin.isdigit() and len(pin) == 4:
            if pin[0] != '0':
                p = 1
            else:
                print("Invalid PIN: The first digit cannot be zero.")
        else:
            print("Invalid PIN: Please enter a 4-digit number.")

    print("To open the account you have to top up at least 200")
    while a != 1:
        balance = get_integer_input("Enter amount to deposit: ")
        if balance >= 200:
            a = 1
        else:
            print("Least amount to deposit is 200")
    agentid = get_integer_input("Enter agent id: ")
    if agentid != agent_id:
        print("incorrect id!!")
        return
    agentpin = get_integer_input("Enter pin: ")
    if agentpin != agent_pin:
        print("Incorect PIN!!")
        return
    transaction = {
        "you have deposited "
        "amount": balance,
        "agent name": agent_name,
        "date": x.strftime("%d %A %B %Y %X"),
        "balance": balance
    }
    store_transaction(transaction)

    account_database['name'] = name
    account_database['phone_number'] = phone_number
    account_database['id'] = idn
    account_database['pin'] = int(pin)
    account_database['balance'] = round(float(balance), 2)
    x = datetime.datetime.now()

    with open(filename, "w") as file:
        json.dump(account_database, file, indent=4)
        print(f"Account created successfully on {x.strftime("%d %A %B %Y %X")} ")
        print(f"account balance is ksh {balance}")


def deposit():
    filename = "Mobile_database.json"

    if os.path.exists(filename):
        if os.path.getsize(filename) == 0:
            print("There is no existing account.")
            print("Consider creating an account")
            return

        else:
            pass

    else:
        print("There is no existing account.")
        print("Consider creating an account")
        return

    x = datetime.datetime.now()
    f = 0
    with open(filename, "r") as file:
        database = json.load(file)
        phone_num = database.get("phone_number")
        names = database.get("name")
        old_bal = database.get("balance")
        id_no = database.get("id")

    while True:
        phone = get_integer_input("Enter phone number to deposit to: ")
        if len(str(phone)) == 9:
            break
        else:
            print("it should be 10 digits")


    if phone == phone_num:
        while f == 0:
            idn = get_integer_input("Enter customers ID number: ")
            if len(str(idn)) == 8:
                f = 1
            else:
                print("ID number should consist of 8 digits!!")

        if not (idn == id_no):
            print("ID number is not correct!!")
            return

        amount = check_account_max()

        agentid = get_integer_input("Enter agent id: ")
        if agentid != agent_id:
            print("incorrect id!!")
            return
        agentpin = get_integer_input("Enter pin: ")
        if agentpin != agent_pin:
            print("Incorect PIN!!")
            return
        print(f"You are about to deposit ksh {amount} to {names} {phone_num}.")
        print("1.To continue")
        print("2.Quit")
        sur = get_integer_input("Enter your choice: ")
        if sur == 1:
            del database["balance"]
            new_bal = round(old_bal + float(amount), 2)
            database["balance"] = new_bal

            with open(filename, "w") as file:
                json.dump(database, file, indent=4)

            transaction = {
                "you have deposited "
                "amount": amount,
                "agent name": agent_name,
                "date": x.strftime("%d %A %B %Y %X"),
                "balance": new_bal
            }
            store_transaction(transaction)

            print(f"You have deposited ksh {amount} to {names} {phone_num} on {x.strftime("%d %A %B %Y %X")}")
        elif sur == 2:
            print("Exiting...")
            return
        else:
            print("Invalid input!!")
            return

    else:
        print("Phone number not associated with account!!")
        return


print("Welcome to Mobile Money Agent")
print("You can deposit you ksh without fee")
while True:
    print("1.Create account")
    print("2.Deposit to account")
    print("3.Quit")
    choice = get_integer_input("Enter your choice: ")

    if choice == 1:
        clear_screen()
        check_mobile_database()

    elif choice == 2:
        clear_screen()
        deposit()

    elif choice == 3:
        clear_screen()
        print("Welcome again👋")
        quit()

    else:
        clear_screen()
        print("Invalid choice")
# agent id and pin