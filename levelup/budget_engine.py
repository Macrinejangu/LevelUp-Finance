class BudgetEngine:
    def __init__(self, ledger):
        self.ledger = ledger
        self.budgets = {}

    def set_budget(self, category, limit):
        if limit < 0:
            raise ValueError("Budget limit cannot be negative")
        self.budgets[category] = limit

    def get_spending_by_category(self):
        transactions = self.ledger.get_transactions()
        spending = {}

        for transaction in transactions:
            amount = transaction["amount"]

            if amount < 0:
                category = transaction["category"]
                spending[category] = spending.get(category, 0) + abs(amount)

        return spending

    def is_over_budget(self, category, limit):
        spending = self.get_spending_by_category()
        return spending.get(category, 0) > limit

    def get_summary(self):
        categories = self.get_spending_by_category()
        total_spent = sum(categories.values())

        over_budget_categories = [
            category
            for category, limit in self.budgets.items()
            if categories.get(category, 0) > limit
        ]

        return {
            "total_spent": total_spent,
            "categories": categories,
            "over_budget_categories": over_budget_categories
        }