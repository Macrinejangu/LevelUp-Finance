"""
TransactionLedger class.
→ A transaction record is a dictionary with keys: id, account_id, amount, category, date.
→ amount is signed: positive = deposit, negative = withdrawal.
"""


class TransactionLedger:
    def __init__(self, account_id):
        pass

    def add_transaction(self, amount, category, date=None):
        pass

    def get_transactions(self, start_date=None, end_date=None):
        pass

    def get_total_by_category(self, category):
        pass
