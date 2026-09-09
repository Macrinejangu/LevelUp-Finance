from levelup.budget_engine import BudgetEngine


class FakeLedger:
    def __init__(self, transactions):
        self.transactions = transactions

    def get_transactions(self, start_date=None, end_date=None):
        return self.transactions


def test_get_spending_by_category():
    ledger = FakeLedger([
        {"amount": -500, "category": "food"},
        {"amount": -300, "category": "food"},
        {"amount": -200, "category": "transport"},
        {"amount": 1000, "category": "income"},
    ])

    engine = BudgetEngine(ledger)

    assert engine.get_spending_by_category() == {
        "food": 800,
        "transport": 200,
    }


def test_is_over_budget():
    ledger = FakeLedger([
        {"amount": -500, "category": "food"},
    ])

    engine = BudgetEngine(ledger)

    assert engine.is_over_budget("food", 400) is True
    assert engine.is_over_budget("food", 600) is False


def test_is_not_over_budget_when_category_has_no_spending():
    ledger = FakeLedger([])

    engine = BudgetEngine(ledger)

    assert engine.is_over_budget("food", 400) is False


def test_get_summary():
    ledger = FakeLedger([
        {"amount": -500, "category": "food"},
        {"amount": -200, "category": "transport"},
    ])

    engine = BudgetEngine(ledger)
    engine.set_budget("food", 400)
    engine.set_budget("transport", 300)

    assert engine.get_summary() == {
        "total_spent": 700,
        "categories": {
            "food": 500,
            "transport": 200,
        },
        "over_budget_categories": ["food"],
    }


def test_set_budget_rejects_negative_limit():
    ledger = FakeLedger([])
    engine = BudgetEngine(ledger)

    try:
        engine.set_budget("food", -100)
        assert False
    except ValueError:
        assert True


def test_zero_spending_is_not_over_budget():
    ledger = FakeLedger([])

    engine = BudgetEngine(ledger)

    assert engine.is_over_budget("food", 0) is False