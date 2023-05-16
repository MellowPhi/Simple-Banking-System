# Simple Banking Systems

import random
import sqlite3


user_option = ""
conn = sqlite3.connect('card.s3db')  # Create a database if it doesn't exist
cur = conn.cursor()  # Create a cursor object
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()
conn.close()


def save_acc(card_no, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    query = 'INSERT INTO card (number, pin) VALUES ({}, {})'.format(card_no, pin)
    cur.execute(query)
    conn.commit()
    conn.close()


def retrieve_acc(card_no, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    query = 'SELECT * FROM card WHERE number = {} AND pin = {} '.format(card_no, pin)
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    return result


def get_acc_bal(card_no, pin):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    query = 'SELECT balance FROM card WHERE number = {} AND pin = {}'.format(card_no, pin)
    cur.execute(query)
    bal = cur.fetchone()
    cur.close()
    for x in bal:
        return x


def add_income(income, card_no):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    query = 'UPDATE card SET balance = balance + {} WHERE number = {}'.format(income, card_no)
    cur.execute(query)
    conn.commit()
    cur.close()


def del_acc(card_no, pin):  # Not sure if this is the right way to delete ACC!
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    query = 'DELETE FROM card where number = {} AND pin = {}'.format(card_no, pin)
    cur.execute(query)
    conn.commit()
    cur.close()


def check_acc(card_no):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    query = 'SELECT EXISTS(SELECT 1 FROM card WHERE number = {})'.format(card_no)
    cur.execute(query)
    result = cur.fetchone()
    cur.close()
    for x in result:
        return x == 1


def transfer(rec_acc, send_acc, amount):
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    query1 = 'UPDATE card SET balance = balance - {} WHERE number = {}'.format(amount, send_acc)
    query2 = 'UPDATE card SET balance = balance + {} WHERE number = {}'.format(amount, rec_acc)
    cur.execute(query1)
    cur.execute(query2)
    conn.commit()
    cur.close()


def luhn_algo(card_no, flag):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_no)
    odd_digits = digits[::2]
    even_digits = digits[1::2]
    total_sum = 0
    total_sum += sum(even_digits)
    for d in odd_digits:
        total_sum += sum(digits_of(d * 2))
    if flag == 0:
        hash_no = str(0) if (total_sum % 10 == 0) else str(10 - (total_sum % 10))
        card_no = int(card_no + hash_no)
        return card_no
    elif flag == 1:
        return total_sum % 10 == 0


def create_account():
    card_no = str(400000000000000 + random.randint(1, 999999999))
    card_no = luhn_algo(card_no, 0)
    pin = random.randint(1000, 9999)
    save_acc(card_no, pin)
    # validity = luhn_algo(card_no, 0)
    # print('validity:',validity)
    return card_no, pin


def login_account():
    login_card_no = int(input("Enter your card no: \n>"))
    login_pin = int(input("Enter your PIN: \n"))
    acc = retrieve_acc(login_card_no, login_pin)
    if acc:
        print("You have successfully logged in!")
        sec_user_option = check_balance(login_card_no, login_pin)
        if sec_user_option == '0':
            return '0'
    else:
        print("Wrong card number or PIN!")


# Stage 4 menu

def check_balance(card_no, pin):
    while True:
        check_balance_option = input("""1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n""")
        if check_balance_option == "1":
            bal = get_acc_bal(card_no, pin)  # Get query from database
            print(f"Balance: {bal}")
        elif check_balance_option == "2":
            income = int(input('Enter income:\n'))
            add_income(income, card_no)
            print('Income was added!')
        elif check_balance_option == "3":
            transfer_acc = int(input('Enter card number:\n'))
            # Check Luhn algorithm to verify if its a vaild card first!
            validity = luhn_algo(transfer_acc, 1)
            if validity is False:
                print('Probably you made a mistake in the card number. Please try again!')
            # If Luhn is passed, check if the card is in the database
            else:
                result = check_acc(transfer_acc)
                if result is False:
                    print('Such a card does not exist.')
                elif card_no == transfer_acc:
                    print("You can't transfer money to the same account!")
                else:
                    amount = int(input('Enter how much money you want to transfer:\n'))
                    bal = get_acc_bal(card_no, pin)
                    if bal < amount:
                        print('Not enough money!')
                    else:
                        transfer(transfer_acc, card_no, amount)
                        print('Success!')
        elif check_balance_option == "4":  # Not sure if this is the right way to delete ACC!
            del_acc(card_no, pin)
            print('The account has been closed!\n')
            break
        elif check_balance_option == "5":
            print("You have successfully logged out!\n")
            break
        elif check_balance_option == "0":
            return '0'


def check_user_option():
    user_option = input("""1. Create an account\n2. Log into account\n0. Exit\n""")
    if user_option == "1":
        # Generate 16 digit card number with 4 digit pin
        card_no, pin = create_account()
        print("""Your card has been created\nYour card number:\n{}\nYour card PIN:\n{}""".format(card_no, pin))
        # print(accounts)

    elif user_option == "2":
        # Prompt for account details and pin
        sec_user_option = login_account()
        if sec_user_option == '0':
            return '0'
    return user_option


if __name__ == '__main__':
    while user_option != "0":
        user_option = check_user_option()
