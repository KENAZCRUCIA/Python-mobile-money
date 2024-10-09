# A Mobile Money menu program
import datetime
import json
import os
import random
import time


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


send_money_list = [
    ("Brian Njeru", "717677103"),
    ("Charles Newton", "745627636"),
    ("Alphonse Waweru", "725257651"),
    ("Aslay Muema", "703525511"),
    ("celine celyne", "715726943"),
    ("Cindy Betty", "708463462")
]

till_numbers = [
    ("MOSES MIGWI NGUGI", "8741162"),
    ("EDITH KANANU BUNDI", "9743007"),
    ("FRIDAH GAKII MICHENI", "9150779")
]


def confirm_phone_name(phone_number, send_money_list):
    for name, number in send_money_list:
        if str(phone_number) == number:
            return name
    return "Unkown"


def confirm_till_number(till_number, till_numbers):
    for name, number in till_numbers:
        if str(till_number) == number:
            return name
    return "Unknown"


def check_mobile_database():
    filename = "Mobile_database.json"

    if os.path.exists(filename):
        if os.path.getsize(filename) == 0:
            with open("mini_statement.txt","w") as file:
                pass

            print("There is no existing account.")
            print("Consider visiting nearby Agent to register account")
            quit()

        else:
            pass

    else:
        print("There is no existing account.")
        print("Consider visiting nearby Agent to register account")
        quit()


def check_maximum(amount):
    if amount >= 250000:
        print("Maximum amount for transaction is 250,000")
        return



def store_transaction(transaction):
    with open("mini_statement.txt", "a") as file:
        file.write(str(transaction) + '\n')


def print_mini_statement():
    with open("mini_statement.txt", "r") as file:
        for line in file:
            print(line.strip())


def transfer_charges(amount):
    charge_table = [
         (1, 49, 0),
         (50, 100, 0,),
         (101, 500, 7),
         (501, 1000, 13),
         (1001, 1500, 23),
         (1501, 2500, 33),
         (2501, 3500, 53),
         (3501, 5000, 57),
         (5001, 7500, 78),
         (7501, 10000, 90),
         (10001, 15000, 100),
         (15001, 20000, 105),
         (20001, 35000, 108),
         (35001, 50000, 108),
         (50001, 250000, 108)
         ]
    for minm, maxm, charge in charge_table:
        if minm <= amount <= maxm:
            return charge
    return "N/A"


def withdraw_charge(amount):
    charge_ranges = [
        (1, 49, "N/A"),
        (50, 100, 11),
        (101, 500, 29),
        (501, 1000, 29),
        (1001, 1500, 29),
        (1501, 2500, 29),
        (2501, 3500, 52),
        (3501, 5000, 69),
        (5001, 7500, 87),
        (7501, 10000, 115),
        (10001, 15000, 167),
        (15001, 20000, 185),
        (20001, 35000, 197),
        (35001, 50000, 278),
        (50001, 250000, 309)
    ]

    for minm, maxm, charge in charge_ranges:
        if minm <= amount <= maxm:
            return charge
    return "N/A"


def check_pin(pin):
    count = 5
    while count > 0:
        new_pin = input("Please enter a 4-digit PIN: ")
        if new_pin.isdigit() and len(new_pin) == 4:
            if int(new_pin) == pin:
                return True
            else:
                count -= 1
                if count == 0:
                    print("You have reached maximum attempts. Try again later.")
                    exit()
                print(f"Invalid PIN: You have {count} attempts remaining.")
        else:
            print("Invalid PIN: Please enter a 4-digit number.")


def get_integer_input(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input.Please enter an integer.")


def send_money():
    while True:
        recipient = get_integer_input("Enter phone number: ")
        if len(str(recipient)) == 9:
            break
        else:
            print("it should be 10 digits")

    amount = get_integer_input("Enter amount to send: ")
    check_maximum(amount)
    charge = transfer_charges(amount)
    rec_name = confirm_phone_name(recipient, send_money_list)
    with open("Mobile_database.json", "r") as file:
        database = json.load(file)
        acbal = database.get('balance')
        if amount >= acbal:
            print("Account balance is too low!!")
            return

        acpin2 = database.get('pin')

    if check_pin(acpin2):
        x = datetime.datetime.now()
        print(f"You are about to send {amount} to {rec_name} {recipient}  .")
        print("To continue press 1.(yes)")
        print("To cancel press 2.(no)")
        sur = int(input("Enter choice: "))
        if sur == 2:
            return
        new_amount = amount + charge

        new_bal = round(acbal - float(new_amount), 2)
        del database['balance']
        database['balance'] = new_bal

        with open("Mobile_database.json", "w") as file:
            json.dump(database, file, indent=4)

        transaction = {
            "you have send "
            "amount": amount,
            "recipient name": rec_name,
            "recipient number": recipient,
            "date": x.strftime("%d %A %B %Y %X"),
            "charge": charge,
            "balance": new_bal
        }
        store_transaction(transaction)

        print("Transaction made successfully")
        print(f"You have send {amount} to {rec_name} {recipient} on {x.strftime("%d %A %B %Y %X")}")
        print(f"Account balance is {new_bal}")


def withdraw_cash():
    agent = get_integer_input("Enter Agent number: ")
    store = get_integer_input("Enter store number: ")
    amount = get_integer_input("Enter amount to withdraw: ")
    check_maximum(amount)
    charge = withdraw_charge(amount)

    if charge == "N/A":
        print("Minimum withdraw is ksh 50.")
        return

    with open("Mobile_database.json", "r") as file:
        database = json.load(file)
        acbal = database.get('balance')
        if amount >= acbal:
            print("Account balance is too low!!")
            return

        acpin2 = database.get('pin')

    if check_pin(acpin2):
        x = datetime.datetime.now()
        print(f"You are about to withdraw ksh {amount} with transaction cost of ksh {charge} "
              f"to Agent number {agent} and store number {store} .")
        print("To continue press 1.(yes)")
        print("To cancel press 2.(no)")
        sur = get_integer_input("Enter choice: ")
        if sur == 2:
            return
        new_amount = amount + charge

        new_bal = round(acbal - float(new_amount), 2)
        del database['balance']
        database['balance'] = new_bal

        with open("Mobile_database.json", "w") as file:
            json.dump(database, file, indent=4)

        transaction = {
            "you have withdrawn "
            "amount": amount,
            "agent number": agent,
            "store number": store,
            "date": x.strftime("%d %A %B %Y %X"),
            "charge": charge,
            "balance": new_bal
        }
        store_transaction(transaction)

        print("Transaction made successfully")
        print(f"You have withdrawn ksh {amount} to {agent} on {x.strftime("%d %A %B %Y %X")} "
              f"transaction cost is ksh {charge}")
        print(f"Account balance is {new_bal}")


def buy_airtime():
    print("1.Buy for my number")
    print("2.Buy for other number")
    airch = int(input("Enter your choice: "))
    x = datetime.datetime.now()

    with open("Mobile_database.json", "r") as file:
        database = json.load(file)
        phone = database.get("phone_number")
        acbal = database.get("balance")
        acpin2 = database.get("pin")

    if airch == 1:
        airt_phone = phone
    elif airch == 2:
        while True:
            airt_phone = get_integer_input("Enter phone number: ")
            if len(str(airt_phone)) == 9:
                break
            else:
                print("it should be 10 digits")

    else:
        print("Invalid choice!!")
        return

    airt_amount = get_integer_input("Enter amount of airtime to buy: ")
    check_maximum(airt_amount)
    if airt_amount >= acbal:
        print("Account balance too low to complete the request!!")
        return
    if check_pin(acpin2):
        new_bal = round(acbal-float(airt_amount), 2)
        del database["balance"]
        database["balance"] = new_bal
        with open("Mobile_database.json", "w") as file:
            json.dump(database, file, indent=4)

        transaction = {
            "you have bought airtime of "
            "airtime amount": airt_amount,
            "phone number": airt_phone,
            "balance": new_bal,
            "date": x.strftime("%d %A %B %Y %X"),
        }
        store_transaction(transaction)

        print("Transaction made successfully")
        print(f"You have bought {airt_amount} to {airt_phone} on {x.strftime("%d %A %B %Y %X")}")
        print(f"Account balance is {new_bal}")


def lipa_na_mpesa():
    print("1.Paybill")
    print("2.Buy goods and services")
    print("3.Pochi la biashara")
    ch = get_integer_input("Enter your choice: ")

    if ch == 1:
        bsnum = get_integer_input("Enter business number: ")
        if len(str(bsnum)) != 6:
            print("It should consist of 6 digits")
            return
        accnum = input("Enter account number: ")
        if len(str(bsnum)) < 4 or len(str(bsnum)) > 9:
            print("It should range between 4 and 10 digits")
            return
        amount = get_integer_input("Enter amount: ")
        check_maximum(amount)
        charge = transfer_charges(amount)
        with open("Mobile_database.json", "r") as file:
            database = json.load(file)
            acbal = database.get('balance')
            if amount >= acbal:
                print("Account balance is too low!!")
                return

            acpin2 = database.get('pin')

        if check_pin(acpin2):
            x = datetime.datetime.now()
            print(f"You are about to send ksh {amount} to Business number {bsnum} and Account number {accnum} "
                  f"transaction cost ksh {charge}.")
            print("To continue press 1.(yes)")
            print("To cancel press 2.(no)")
            sur = get_integer_input("Enter choice: ")
            if sur == 2:
                return

            new_bal = round(acbal - (float(amount) + charge), 2)
            del database['balance']
            database['balance'] = new_bal

            with open("Mobile_database.json", "w") as file:
                json.dump(database, file, indent=4)

            transaction = {
                "you have paid "
                "amount": amount,
                "business snumber": bsnum,
                "date": x.strftime("%d %A %B %Y %X"),
                "charge": charge,
                "balance": new_bal
            }
            store_transaction(transaction)

            print("Transaction made successfully")
            print(f"You have send ksh {amount} to {bsnum} on {x.strftime("%d %A %B %Y %X")} "
                  f"transaction cost ksh {charge}")
            print(f"Account balance is {new_bal}")

    elif ch == 2:
        till_num = get_integer_input("Enter till number: ")
        if len(str(till_num)) != 7:
            print("It should consist of 7 digits")
            return
        amount = get_integer_input("Enter amount: ")
        check_maximum(amount)
        charge = transfer_charges(amount)
        till_name = confirm_till_number(till_num, till_numbers)
        with open("Mobile_database.json", "r") as file:
            database = json.load(file)
            acbal = database.get('balance')
            if amount >= acbal:
                print("Account balance is too low!!")
                return

            acpin2 = database.get('pin')

        if check_pin(acpin2):
            x = datetime.datetime.now()
            print(f"You are about to send ksh {amount} to Till number {till_num} {till_name} transaction cost ksh {charge}.")
            print("To continue press 1.(yes)")
            print("To cancel press 2.(no)")
            sur = get_integer_input("Enter choice: ")
            if sur == 2:
                return

            new_bal = round(acbal - (float(amount) + charge), 2)
            del database['balance']
            database['balance'] = new_bal

            with open("Mobile_database.json", "w") as file:
                json.dump(database, file, indent=4)

            transaction = {
                "you have paid "
                "amount": amount,
                "Till name": till_name,
                "Till number": till_num,
                "date": x.strftime("%d %A %B %Y %X"),
                "charge": charge,
                "balance": new_bal
            }
            store_transaction(transaction)

            print("Transaction made successfully")
            print(f"You have send ksh {amount} to {till_num} {till_name} on {x.strftime("%d %A %B %Y %X")} "
                  f"transaction cost ksh {charge}")
            print(f"Account balance is {new_bal}")

    elif ch == 3:
        while True:
            pochi = get_integer_input("Enter phone number: ")
            if len(str(pochi)) == 9:
                break
            else:
                print("it should be 10 digits")

        amount = get_integer_input("Enter amount: ")
        check_maximum(amount)
        charge = transfer_charges(amount)
        poch_name = confirm_phone_name(pochi, send_money_list)
        with open("Mobile_database.json", "r") as file:
            database = json.load(file)
            acbal = database.get('balance')
            if amount >= acbal:
                print("Account balance is too low!!")
                return

            acpin2 = database.get('pin')

        if check_pin(acpin2):
            x = datetime.datetime.now()
            print(f"You are about to send ksh {amount} to pochi number {pochi} {poch_name} transaction cost ksh {charge} .")
            print("To continue press 1.(yes)")
            print("To cancel press 2.(no)")
            sur = get_integer_input("Enter choice: ")
            if sur == 2:
                return

            new_bal = round(acbal - (float(amount) + charge), 2)
            del database['balance']
            database['balance'] = new_bal

            with open("Mobile_database.json", "w") as file:
                json.dump(database, file, indent=4)

            transaction = {
                "you have paid "
                "amount": amount,
                "pochi name": poch_name,
                "Pochi number": pochi,
                "date": x.strftime("%d %A %B %Y %X"),
                "charge": charge,
                "balance": new_bal
            }
            store_transaction(transaction)

            print("Transaction made successfully")
            print(f"You have send ksh {amount} to {pochi} {poch_name} on {x.strftime("%d %A %B %Y %X")} "
                  f"transaction cost ksh {charge}")
            print(f"Account balance is {new_bal}")

    else:
        print("Invalid choice!!")
        return


def my_account():
    x = datetime.datetime.now()
    print("1.Check balance")
    print("2.Change PIN")
    print("3.Print Mini statement")
    m_choice = get_integer_input("Enter your choice: ")

    if m_choice == 1:
        with open("Mobile_database.json", "r") as file:
            database = json.load(file)
            acc_p = database.get("pin")
            acc_bal = database.get("balance")

        if check_pin(acc_p):
            print(f"Your account balance is {acc_bal} on {x.strftime("%d %A %B %Y %X")} .")

    elif m_choice == 2:
        with open("Mobile_database.json", "r") as file:
            database = json.load(file)
            old_p = database.get("pin")
        if check_pin(old_p):
            print("You will receive OTP shortly.")
            print("DO NOT SHARE")
            print("It will be valid within 6 second.")
            time.sleep(3)
            random_digits = random.randint(1000, 9000)
            print(random_digits)
            time.sleep(6)
            otp = get_integer_input("Enter the OTP we just sent: ")
            if otp == random_digits:
                while True:
                    new_pin = input("Please enter a 4-digit new PIN: ")

                    if new_pin.isdigit() and len(new_pin) == 4:
                        if new_pin[0] != '0':
                            print("Valid PIN entered.")
                            break
                        else:
                            print("Invalid PIN: The first digit cannot be zero.")
                    else:
                        print("Invalid PIN: Please enter a 4-digit number.")

                del database["pin"]
                database["pin"] = int(new_pin)

                with open("Mobile_database.json", "w") as file:
                    json.dump(database, file, indent=4)
                print(f"PIN changed successfully on {x.strftime("%d %A %B %Y %X")}")

            else:
                print("Invalid OTP!!")
                return
        else:
            print("Incorrect PIN!!")
            print("If you may have forgot you may consider")
            print("conducting customer care though")
            print("  100 or 400")
            return

    elif m_choice == 3:
        print_mini_statement()
        return
    else:
        print("Invalid choice!!")
        return


def customer_care():
    with open("Mobile_database.json", "r") as file:
        database = json.load(file)
        bal = database.get("balance")
        idn = database.get("id")
    print("Welcome to customer care services")
    print("We have to ask you some questions to verify if you are the owner")
    idno = get_integer_input("Enter your ID number: ")
    if idno != idn:
        print("Suspicious activity!!")
        quit()
    cou = 2
    while cou != 0:
        am = get_integer_input("Enter your estimated account balance: ")
        if not (am < (am + 500) and am > (am - 500)):
            print("Your estimation is wrong!!")
            cou -= 1
        else:
            cou = 0

    print("You will receive OTP shortly")
    print("DO NOT SHARE")
    print("It will be valid within 6 second.")
    time.sleep(5)
    x = datetime.datetime.now()
    random_digits = random.randint(1000, 9000)
    print(random_digits)
    time.sleep(6)
    otp = get_integer_input("Enter the OTP we just sent: ")
    if otp == random_digits:
        while True:
            new_pin = input("Please enter a 4-digit PIN: ")

            if new_pin.isdigit() and len(new_pin) == 4:
                if new_pin[0] != '0':
                    print("Valid PIN entered.")
                    break
                else:
                    print("Invalid PIN: The first digit cannot be zero.")
            else:
                print("Invalid PIN: Please enter a 4-digit number.")

        del database["pin"]
        database["pin"] = int(new_pin)

        with open("Mobile_database.json", "w") as file:
            json.dump(database, file, indent=4)
        print(f"PIN changed successfully on {x.strftime("%d %A %B %Y %X")}")

    else:
        print("Invalid OTP!!")
        return


while True:
    check_mobile_database()

    print("* * * * * * * * * _")
    print("*      MENU        *")
    print("* 1.Send Money     *")
    print("* 2.Withdraw Cash  *")
    print("* 3.Buy Airtime    *")
    print("* 4.Lipa na M-pesa *")
    print("* 5.My account     *")
    print("* 6.Quit           *")
    print("_ * * * * * * * _")
    print()
    choice = get_integer_input("Enter your choice: ")
    if choice == 1:
        clear_screen()
        send_money()
        time.sleep(3)
    elif choice == 2:
        clear_screen()
        withdraw_cash()
        time.sleep(3)
    elif choice == 3:
        clear_screen()
        buy_airtime()
        time.sleep(3)
    elif choice == 4:
        clear_screen()
        lipa_na_mpesa()
        time.sleep(3)
    elif choice == 5:
        clear_screen()
        my_account()
        time.sleep(3)
    elif choice == 100 or choice == 400:
        clear_screen()
        print("USSD code running...")
        time.sleep(5)
        customer_care()
        time.sleep(3)
    elif choice == 6:
        time.sleep(1)
        clear_screen()
        print("Welcome again 🤝")
        break
    else:
        clear_screen()
        print("Invalid choice!!")

#Next updates:
#   buy airtime pin requirement |/
#   transaction cost|/
#   maximum account balance 500,000.00 |/
#   Maximum money per transaction 250,000.00 |/
#   mini statement |/
#   wrong mpesa pin 5 times and account lock |/
#   to register account need ID number. |/
#   for forgot password ID number needed and security questions