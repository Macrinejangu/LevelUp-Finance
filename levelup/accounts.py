
class Account:
    def __init__(self, name: str, balance: float = 0):
        self.name = name
        self.balance = balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be a number greater than zero")
        self.balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be a number greater than zero")
        if amount > self.balance:
            raise ValueError(" You currently have Insufficient funds")
        self.balance -= amount

    def apply_monthly(self):
        """Override in subclasses. Returns amount changed."""
        return 0


class SavingsAccount(Account):
    def apply_monthly(self):
        interest = self.balance * 0.005 if self.balance > 0 else 0
        self.balance += interest
        return interest



class CheckingAccount(Account):
    def apply_monthly(self):
        if self.balance < 100:
            self.balance -= 5
            return -5
        return 0


class CreditAccount(Account):
    credit_limit: float = 1000

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance + self.credit_limit:
            raise ValueError("Over credit limit")
        self.balance -= amount

    def apply_monthly(self):
        if self.balance < 0:
            interest = abs(self.balance) * 0.015
            self.balance -= interest
            return -interest
        return 0