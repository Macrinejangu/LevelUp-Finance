"""
Quest classes.
→ Base Quest class, plus DailyQuest, WeeklyQuest, BossQuest.
"""


class Quest:
    def __init__(self, name, reward_xp):
        pass

    def check_completion(self, ledger):
        pass

    def get_reward(self):
        pass


class DailyQuest(Quest):
    def check_completion(self, ledger):
        pass


class WeeklyQuest(Quest):
    def check_completion(self, ledger):
        pass


class BossQuest(Quest):
    def check_completion(self, ledger):
        pass

    # → returns how close to the target, boss battles show a progress bar
    def get_progress(self, ledger):
        pass
