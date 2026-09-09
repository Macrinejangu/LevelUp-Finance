"""
TransactionLedger class.

A transaction record is a dictionary with keys: id, account_id, amount, category, date.
amount is signed: positive = deposit, negative = withdrawal.
"""

from datetime import date


class TransactionLedger:
    def __init__(self, account_id):
        self.account_id = account_id  #the init method acts automatically thus a number is autiomatically passed when a new ledger is created
        self.transactions = [] #This creates an empty list where transactions will be storef

    def add_transaction(self, amount, category, date_str=None): #(date_str=None) means that the date is optional to add 
        if date_str is None:
            date_str = date.today().isoformat() #this is the ISO format 2026-09-11
#if the person fails to indicate the date the ledger will automatically use the current date like saaa hiiiii
        self.transactions.append({
            "id": len(self.transactions) + 1, #adds onto the number of transactions belonging to another account
            "account_id": self.account_id, #it tells you which account the transaction belongs to
            "amount": amount,
            "category": category,
            "date": date_str,
        })
#Retrieving the particular transaction 
    def get_transactions(self, start_date=None, end_date=None):
        result = self.transactions[:]  #this makes a copy of the transactions then filtering is possible if the user provided the dates   
        if start_date:
            result = [transaction for transaction in result if transaction["date"] >= start_date] #it filkters the list of transactions to the particular start date
        if end_date:
            result = [transaction for transaction in result if transaction["date"] <= end_date] #it filters the list of transactions from the start date to the particular end date
        return result

    def get_total_by_category(self, category):
        total = 0
        for t in self.transactions: #it shows to go through every transaction
            if t["category"] == category: #for checking whether the transaction belongs to a particular category
                total += t["amount"]
        return total