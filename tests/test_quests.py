from datetime import date, timedelta

from levelup.quests import (
    Quest,
    DailyQuest,
    WeeklyQuest,
    BossQuest,
)


class FakeLedger:
    def __init__(self, transactions):
        self.transactions = transactions

    def get_transactions(self, start_date=None, end_date=None):
        if start_date is None and end_date is None:
            return self.transactions

        filtered = []

        for transaction in self.transactions:
            transaction_date = transaction["date"]

            if start_date is not None and transaction_date < start_date:
                continue

            if end_date is not None and transaction_date > end_date:
                continue

            filtered.append(transaction)

        return filtered


def test_quest_get_reward():
    quest = Quest("Test Quest", 100)

    assert quest.get_reward() == 100


def test_quest_base_check_completion():
    quest = Quest("Test Quest", 100)

    try:
        quest.check_completion(FakeLedger([]))
        assert False
    except NotImplementedError:
        assert True


def test_daily_quest_completed_today():
    today = date.today().isoformat()

    ledger = FakeLedger([
        {
            "date": today,
            "amount": -100,
            "category": "food",
        }
    ])

    quest = DailyQuest("Log today's transactions", 25)

    assert quest.check_completion(ledger) is True


def test_daily_quest_not_completed_without_today_transaction():
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    ledger = FakeLedger([
        {
            "date": yesterday,
            "amount": -100,
            "category": "food",
        }
    ])

    quest = DailyQuest("Log today's transactions", 25)

    assert quest.check_completion(ledger) is False


def test_weekly_quest_completed_this_week():
    today = date.today().isoformat()

    ledger = FakeLedger([
        {
            "date": today,
            "amount": -100,
            "category": "food",
        }
    ])

    quest = WeeklyQuest("Log transactions this week", 50)

    assert quest.check_completion(ledger) is True


def test_weekly_quest_not_completed_with_old_transaction():
    old_date = (
        date.today() - timedelta(days=8)
    ).isoformat()

    ledger = FakeLedger([
        {
            "date": old_date,
            "amount": -100,
            "category": "food",
        }
    ])

    quest = WeeklyQuest("Log transactions this week", 50)

    assert quest.check_completion(ledger) is False


def test_boss_quest_progress():
    ledger = FakeLedger([
        {
            "date": date.today().isoformat(),
            "amount": -500,
            "category": "savings",
        }
    ])

    quest = BossQuest("Save 1000", 200, 1000)

    assert quest.get_progress(ledger) == 500


def test_boss_quest_completed():
    ledger = FakeLedger([
        {
            "date": date.today().isoformat(),
            "amount": -600,
            "category": "savings",
        },
        {
            "date": date.today().isoformat(),
            "amount": -500,
            "category": "savings",
        }
    ])

    quest = BossQuest("Save 1000", 200, 1000)

    assert quest.check_completion(ledger) is True


def test_boss_quest_not_completed():
    ledger = FakeLedger([
        {
            "date": date.today().isoformat(),
            "amount": -600,
            "category": "savings",
        }
    ])

    quest = BossQuest("Save 1000", 200, 1000)

    assert quest.check_completion(ledger) is False


def test_boss_quest_progress_does_not_exceed_target():
    ledger = FakeLedger([
        {
            "date": date.today().isoformat(),
            "amount": -1500,
            "category": "savings",
        }
    ])

    quest = BossQuest("Save 1000", 200, 1000)

    assert quest.get_progress(ledger) == 1000