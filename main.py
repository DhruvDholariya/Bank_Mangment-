import json
import string
import random
from pathlib import Path


class Bank:
   
    database = 'data.json'
    data = []

    try:

        if Path(database).exists():

            with open(database) as fs:
                data =json.loads(fs.read())

        else:
            print("file not found")

    except Exception as err:
        print(err)

    @staticmethod
    def __update():
        with open(Bank.database,'w') as fs:
            fs.write(json.dumps(Bank.data))

    @staticmethod
    def __generate_account_number():
        alphabet = random.choices(string.ascii_letters,k=4)
        digits = random.choices(string.digits,k=3)
        spchar = random.choices("!@#$%^&*",k=2)
        id = alphabet + digits + spchar
        random.shuffle(id)
        return ''.join(id)
    
    def create_account(self):
        user_data = {
            "name" : input("enter your name : "),
            "age" : int(input("enter your age : ")),
            "gender" : input("enter your gender : "),
            "email" : input("enter your email : "),
            "pin" : input("enter your pin : "),
            "account_number" : Bank.__generate_account_number(),
            "balance" : 0
        }

        if user_data['age'] < 18 or len(str(user_data['pin'])) != 4:
                print("you are not eligible to create an account")
        else:
            print("account created successfully !!")
            for i in user_data:
                print(f"{i} : {user_data[i]}")
            print("please note down your account number for future reference")
            Bank.data.append(user_data)
            Bank.__update()

    def deposit(self):
        accountno = input("enter your account number : ")
        pin = input("enter your pin : ")
      
        userdata = [i for i in Bank.data if i['account_number'] == accountno and i['pin'] == pin]    

        if userdata == []:
            print("user data not found")
                
        else:
            amount = int(input("Enter the amount you want to deposit : "))

            if amount <0 or amount > 10000:
                print("invalid amount")
            else:
                userdata[0]['balance'] += amount
                Bank.__update()
                print("amount deposited successfully")

    def withdraw(self):
        accountno = input("enter your account number : ")
        pin = input("enter your pin : ")

        userdata = [i for i in Bank.data if i['account_number'] == accountno and i['pin'] == pin]

        if userdata == []:
            print("user data not found")
        else:
            amount = int(input("Enter the amount you want to withdraw : "))

            if amount < 0 or amount > 10000:
                print("invalid amount")
            elif amount > userdata[0]['balance']:
                print("insufficient balance")
            else:
                userdata[0]['balance'] -= amount
                Bank.__update()
                print("amount withdrawn successfully")

    def account_details(self):
        accountno = input("enter your account number : ")
        pin = input("enter your pin : ")

        userdata = [i for i in Bank.data if i['account_number'] == accountno and i['pin'] == pin]

        if userdata == []:
            print("user data not found")
        else:
            print("account details are as follows : ")
            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")

    def update_account(self):
        accountno = input("enter your account number : ")
        pin = input("enter your pin : ")

        userdata = [i for i in Bank.data if i['account_number'] == accountno and i['pin'] == pin]

        if userdata == []:
            print("user data not found")
        else:
            print("press 1 for updating name")
            print("press 2 for updating email")
            print("press 3 for updating pin")
            print("press 4 for updating age")
            print("press 5 for updating gender")

            check = int(input("enter your choice : "))

            if check == 1:
                new_name  = input("enter your new name : ")
                userdata[0]['name'] = new_name
                Bank.__update()
                print("name updated successfully")
            elif check == 2:
                new_email = input("enter your new email : ")
                userdata[0]['email'] = new_email
                Bank.__update()
                print("email updated successfully")
            elif check == 3:
                new_pin = input("enter your new pin : ")
                if len(str(new_pin)) != 4:
                    print("invalid pin")
                else:
                    userdata[0]['pin'] = new_pin
                    Bank.__update()
                    print("pin updated successfully")
            elif check == 4:
                new_age = int(input("enter your new age : "))
                if new_age < 18:
                    print("you are not eligible to update your age")
                else:
                    userdata[0]['age'] = new_age
                    Bank.__update()
                    print("age updated successfully")
            elif check == 5:
                new_gender = input("enter your new gender : ")
                userdata[0]['gender'] = new_gender
                Bank.__update()
                print("gender updated successfully")

    def delete_account(self):
        accountno = input("enter your account number : ")
        pin = input("enter your pin : ")

        userdata = [i for i in Bank.data if i['account_number'] == accountno and i['pin'] == pin]

        if userdata == []:
            print("user data not found")
        else:
            Bank.data.remove(userdata[0])
            Bank.__update()
            print("account deleted successfully")

user = Bank()

print("press 1 for create a new account")
print("press 2 for deposit an amount")
print("press 3 for withdraw an amount")
print("press 4 for details of the account")
print("press 5 for updating the account details")
print("press 6 for deleting the account")

check = int(input("enter your choice: "))

if check == 1:
    user.create_account()
elif check == 2:
    user.deposit()
elif check == 3:
    user.withdraw()
elif check == 4:
    user.account_details()
elif check == 5:
    user.update_account()
elif check == 6:
    user.delete_account()
else:
    print("invalid choice")