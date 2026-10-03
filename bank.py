import json
import random
import string
from pathlib import Path


class Bank:

    database = "data.json"

    def __init__(self):
        self.data = self.load_data()

    # ---------------- LOAD DATA ----------------
    def load_data(self):
        try:
            if Path(self.database).exists():
                with open(self.database, "r") as file:
                    return json.load(file)

            return []

        except (json.JSONDecodeError, OSError) as err:
            print(f"Error loading data: {err}")
            return []

    # ---------------- SAVE DATA ----------------
    def save_data(self):
        try:
            with open(self.database, "w") as file:
                json.dump(self.data, file, indent=4)

        except OSError as err:
            print(f"Error saving data: {err}")

    # ---------------- GENERATE ACCOUNT NUMBER ----------------
    @staticmethod
    def generate_account_number():

        alphabet = random.choices(string.ascii_uppercase, k=4)
        digits = random.choices(string.digits, k=3)
        special = random.choices("!@#$%^&*", k=2)

        account_id = alphabet + digits + special

        random.shuffle(account_id)

        return "".join(account_id)

    # ---------------- FIND ACCOUNT ----------------
    def find_account(self, account_number, pin):

        for account in self.data:

            if (
                account["account_number"] == account_number
                and account["pin"] == pin
            ):
                return account

        return None

    # ---------------- CREATE ACCOUNT ----------------
    def create_account(
        self,
        name,
        age,
        gender,
        email,
        pin
    ):

        if age < 18:
            return False, "You must be 18 or older."

        if not pin.isdigit() or len(pin) != 4:
            return False, "PIN must contain exactly 4 digits."

        # Check duplicate email
        for account in self.data:

            if account["email"] == email:
                return False, "Email already registered."

        account = {
            "name": name,
            "age": age,
            "gender": gender,
            "email": email,
            "pin": pin,
            "account_number": self.generate_account_number(),
            "balance": 0
        }

        self.data.append(account)
        self.save_data()

        return True, account

    # ---------------- DEPOSIT ----------------
    def deposit(self, account_number, pin, amount):

        account = self.find_account(account_number, pin)

        if account is None:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Amount must be greater than 0."

        if amount > 10000:
            return False, "Maximum deposit is ₹10,000."

        account["balance"] += amount

        self.save_data()

        return True, account["balance"]

    # ---------------- WITHDRAW ----------------
    def withdraw(self, account_number, pin, amount):

        account = self.find_account(account_number, pin)

        if account is None:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Amount must be greater than 0."

        if amount > 10000:
            return False, "Maximum withdrawal is ₹10,000."

        if amount > account["balance"]:
            return False, "Insufficient balance."

        account["balance"] -= amount

        self.save_data()

        return True, account["balance"]

    # ---------------- ACCOUNT DETAILS ----------------
    def get_account(self, account_number, pin):

        account = self.find_account(account_number, pin)

        if account is None:
            return False, "Invalid account number or PIN."

        return True, account

    # ---------------- UPDATE ACCOUNT ----------------
    def update_account(
        self,
        account_number,
        pin,
        field,
        value
    ):

        account = self.find_account(account_number, pin)

        if account is None:
            return False, "Invalid account number or PIN."

        if field == "name":

            if not value.strip():
                return False, "Name cannot be empty."

            account["name"] = value

        elif field == "email":

            if not value.strip():
                return False, "Email cannot be empty."

            account["email"] = value

        elif field == "pin":

            if not value.isdigit() or len(value) != 4:
                return False, "PIN must contain exactly 4 digits."

            account["pin"] = value

        elif field == "age":

            age = int(value)

            if age < 18:
                return False, "Age must be 18 or above."

            account["age"] = age

        elif field == "gender":

            account["gender"] = value

        else:
            return False, "Invalid field."

        self.save_data()

        return True, "Account updated successfully."

    # ---------------- DELETE ACCOUNT ----------------
    def delete_account(self, account_number, pin):

        account = self.find_account(account_number, pin)

        if account is None:
            return False, "Invalid account number or PIN."

        self.data.remove(account)

        self.save_data()

        return True, "Account deleted successfully."