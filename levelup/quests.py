from datetime import date, timedelta


class Quest:
    def __init__(self, name, reward_xp):
        self.name = name
        self.reward_xp = reward_xp

    def check_completion(self, ledger):
        raise NotImplementedError

    def get_reward(self):
        return self.reward_xp


class DailyQuest(Quest):
    def check_completion(self, ledger):
        today = date.today().isoformat()
        transactions = ledger.get_transactions(
            start_date=today,
            end_date=today
        )
        return len(transactions) > 0


class WeeklyQuest(Quest):
    def check_completion(self, ledger):
        today = date.today()
        week_start = today - timedelta(days=today.weekday())

        transactions = ledger.get_transactions(
            start_date=week_start.isoformat(),
            end_date=today.isoformat()
        )

        return len(transactions) > 0


class BossQuest(Quest):
    def __init__(self, name, reward_xp, target_amount):
        super().__init__(name, reward_xp)
        self.target_amount = target_amount

    def get_progress(self, ledger):
        transactions = ledger.get_transactions()
        total = sum(transaction["amount"] for transaction in transactions)

        return min(abs(total), self.target_amount)

    def check_completion(self, ledger):
        return self.get_progress(ledger) >= self.target_amount