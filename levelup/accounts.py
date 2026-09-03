"""
Account classes.
→ Base Account class, plus SavingsAccount, CheckingAccount, CreditAccount.
→ Interfaces agreed as a team, Sprint 1, Day 1.
→ withdraw() raises ValueError if amount exceeds balance or is negative.
"""


class Account:
    def __init__(self, name, balance=0):
        pass

    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass

    def get_balance(self):
        pass

    # → meant to be overridden by each subclass
    def calculate_fee_or_interest(self):
        pass


class SavingsAccount(Account):
    def calculate_fee_or_interest(self):
        pass


class CheckingAccount(Account):
    def calculate_fee_or_interest(self):
        pass


class CreditAccount(Account):
    def calculate_fee_or_interest(self):
        pass
