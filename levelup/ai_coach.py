"""
AICoach class.
→ Hard rule: narrate() only ever receives a plain dictionary of already-computed
  results, e.g. {"quest_completed": "Shield Block", "xp_gained": 25}.
→ It never receives a ledger, an account, or a Quest object directly.
  This is what keeps the AI from being able to influence scoring.
"""


class AICoach:
    def __init__(self, backend_client):
        pass

    def narrate(self, summary):
        pass
