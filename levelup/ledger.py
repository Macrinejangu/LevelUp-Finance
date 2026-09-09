"""
TransactionLedger class.
→ A transaction record is a dictionary with keys: id, account_id, amount, category, date.
→ amount is signed: positive = deposit, negative = withdrawal.
→ Persists to SQLite via save() and load(), same pattern as PlayerProfile.
"""
from datetime import date
from levelup.database import get_connection


class TransactionLedger:
    def __init__(self, account_id):
        self.account_id = account_id
        self.transactions = []

    def add_transaction(self, amount, category, date_str=None):
        if date_str is None:
            date_str = date.today().isoformat()

        self.transactions.append({
            "id": len(self.transactions) + 1,
            "account_id": self.account_id,
            "amount": amount,
            "category": category,
            "date": date_str,
        })

    def get_transactions(self, start_date=None, end_date=None):
        result = self.transactions[:]
        if start_date:
            result = [t for t in result if t["date"] >= start_date]
        if end_date:
            result = [t for t in result if t["date"] <= end_date]
        return result

    def get_total_by_category(self, category):
        total = 0
        for t in self.transactions:
            if t["category"] == category:
                total += t["amount"]
        return total

    def save(self):
        conn = get_connection()

        # → delete this account's existing rows first, then reinsert everything
        #   currently in memory, this keeps the database and self.transactions
        #   perfectly in sync without needing to track which ones are "new"
        conn.execute("DELETE FROM transactions WHERE account_id = ?", (self.account_id,))

        for transaction in self.transactions:
            conn.execute(
                """
                INSERT INTO transactions (account_id, amount, category, date)
                VALUES (?, ?, ?, ?)
                """,
                (
                    transaction["account_id"],
                    transaction["amount"],
                    transaction["category"],
                    transaction["date"],
                ),
            )

        conn.commit()
        conn.close()

    def load(self):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT id, account_id, amount, category, date
            FROM transactions
            WHERE account_id = ?
            ORDER BY id
            """,
            (self.account_id,),
        ).fetchall()
        conn.close()

        # → the ids here come from the database's own auto-increment, not
        #   the len(self.transactions) + 1 count used when adding in memory,
        #   loading always reflects what's actually saved
        self.transactions = [
            {"id": row[0], "account_id": row[1], "amount": row[2], "category": row[3], "date": row[4]}
            for row in rows
        ]


# → quick manual test, run this from the project root with:
#   python3 -m levelup.ledger
if __name__ == "__main__":
    ledger = TransactionLedger(account_id=1)
    ledger.add_transaction(-500, "food")
    ledger.add_transaction(2000, "income")

    print("Before save:", ledger.get_transactions())

    ledger.save()
    print("Saved to database.")

    reloaded = TransactionLedger(account_id=1)
    reloaded.load()
    print("After reload:", reloaded.get_transactions())
#the changes are now updated in the database