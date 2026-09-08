"""
AICoach class.
→ Hard rule: narrate() only ever receives a plain dictionary of already-computed
  results, e.g. {"event": "quest_completed", "quest_name": "Shield Block", "xp_gained": 25}.
→ It never receives a ledger, an account, or a Quest object directly.
  This is what keeps the AI from being able to influence scoring, it only
  describes what already happened, it never decides what happened.
→ Backend: Ollama, running locally. Model: phi4-mini, decided as a team.
→ Tone: geeky, comical, quest-styled, in the spirit of the Fireship YouTube channel.
"""
import ollama


class AICoach:
    def __init__(self, backend_client="phi4-mini"):
        # → backend_client is just the model name, Ollama runs the actual model
        #   locally in the background, we're only telling it which one to use
        self.model = backend_client
        self._system_prompt = self._build_system_prompt()

    def narrate(self, summary):
        # → wrapped in try/except on purpose: if Ollama isn't running for
        #   whatever reason, the game should still work, just without flair
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._system_prompt},
                    {"role": "user", "content": self._build_user_message(summary)},
                ],
            )
            return response["message"]["content"]
        except Exception:
            return self._fallback_message(summary)

    def _build_system_prompt(self):
        return (
            "You are the AI coach in a gamified personal finance app. "
            "Your job is to narrate financial events in one or two short sentences, "
            "in a tone that is witty, geeky, and comical, similar to how the Fireship "
            "YouTube channel talks about tech, quick, clever, a little deadpan, never "
            "sincere or formal.\n\n"
            "Hard rules:\n"
            "1. Only use the numbers and names given to you. Never invent a figure "
            "that wasn't provided.\n"
            "2. Never give financial advice, you are narrating what already "
            "happened, not recommending what to do next.\n"
            "3. Keep it to one or two sentences, no long paragraphs.\n\n"
            "Examples of the tone to match:\n"
            "- 'Shield Block secured. Your wallet just dodged a bullet it didn't "
            "even see coming.'\n"
            "- 'Level 4 unlocked. Somewhere, a compound interest calculator just "
            "shed a single, proud tear.'\n"
            "- 'Streak reset to zero. It's fine. Everything is fine. Log today's "
            "spending and let's pretend this didn't happen.'"
        )

    def _build_user_message(self, summary):
        return f"Narrate this event for the player: {summary}"

    def _fallback_message(self, summary):
        # → plain, honest message if the AI backend is unreachable,
        #   the app keeps working, it just sounds like a normal notification
        event = summary.get("event", "update")
        return f"[{event}] {summary}"


# → quick manual test, run this file directly to check the connection works
if __name__ == "__main__":
    coach = AICoach()
    test_summary = {"event": "quest_completed", "quest_name": "Shield Block", "xp_gained": 25}
    print(coach.narrate(test_summary))