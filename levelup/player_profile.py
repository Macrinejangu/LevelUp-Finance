"""
PlayerProfile class.
→ Tracks XP, level, and streak.
→ Persists to SQLite via save() and load().
→ XP curve: leveling from N to N+1 needs current_level * 150 XP.
→ Streak: +5 XP per consecutive day logged, +50 bonus every 7 days,
  resets to 0 if a day is missed. Decided as a team, borrowed from
  Fortune City's streak mechanic.
"""
from datetime import date
from levelup.database import get_connection


class PlayerProfile:
    def __init__(self, name):
        self.name = name
        self.xp = 0
        self.level = 1
        self.streak = 0
        self.last_active_date = None

    def add_xp(self, amount):
        self.xp += amount
        leveled_up = None
        xp_needed = self.level * 150

        # → a single add_xp call can push through more than one level,
        #   the while loop handles that instead of just checking once
        while self.xp >= xp_needed:
            self.xp -= xp_needed
            self.level += 1
            leveled_up = self.level
            xp_needed = self.level * 150

        return leveled_up

    def get_level(self):
        return self.level

    def get_xp(self):
        return self.xp

    # → call this once per day a transaction gets logged
    # → returns the bonus XP earned from the streak this call
    def update_streak(self, today=None):
        if today is None:
            today = date.today()

        if self.last_active_date is None:
            self.streak = 1
        else:
            days_since = (today - self.last_active_date).days
            if days_since == 1:
                self.streak += 1
            elif days_since == 0:
                pass  # already logged today, streak doesn't change twice
            else:
                self.streak = 1  # streak broken, restart

        self.last_active_date = today

        bonus_xp = 5
        if self.streak % 7 == 0:
            bonus_xp += 50  # weekly milestone bonus

        self.add_xp(bonus_xp)
        return bonus_xp

    def save(self):
        conn = get_connection()
        conn.execute(
            """
            UPDATE player_profile
            SET xp = ?, level = ?, streak = ?, last_active_date = ?
            WHERE id = 1
            """,
            (
                self.xp,
                self.level,
                self.streak,
                self.last_active_date.isoformat() if self.last_active_date else None,
            ),
        )
        conn.commit()
        conn.close()

    def load(self):
        conn = get_connection()
        row = conn.execute(
            "SELECT xp, level, streak, last_active_date FROM player_profile WHERE id = 1"
        ).fetchone()
        conn.close()

        if row:
            self.xp, self.level, self.streak, last_active = row
            self.last_active_date = date.fromisoformat(last_active) if last_active else None