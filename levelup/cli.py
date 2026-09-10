"""
CLI menu and command routing.
→ Ties every module together into the terminal game loop.
→ Logging a transaction now checks daily/weekly quest completion and
  awards XP automatically, then the AI coach narrates it.
"""
from levelup.database import init_db, get_connection
from levelup.accounts import SavingsAccount, CheckingAccount, CreditAccount
from levelup.ledger import TransactionLedger
from levelup.budget_engine import BudgetEngine
from levelup.quests import DailyQuest, WeeklyQuest
from levelup.player_profile import PlayerProfile
from levelup.ai_coach import AICoach


def get_valid_number(prompt):
    while True:
        raw_value = input(prompt)
        try:
            return float(raw_value)
        except ValueError:
            print(f"'{raw_value}' isn't a number, try again.")


def show_menu():
    print("\n=== LevelUp Finance ===")
    print("1. Create an account")
    print("2. View balance")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Log a transaction")
    print("6. View budget summary")
    print("7. View my profile")
    print("8. Talk to my AI coach")
    print("9. Exit")


def main():
    init_db()

    account = None
    ledger = None
    budget_engine = None

    # → standing quests for this session, checked every time a transaction gets logged. Awarded flags are in-memory only, they reset if the app restarts, that's a known limitation, not a finished feature.
    daily_quest = DailyQuest("Log today's transactions", 25)
    weekly_quest = WeeklyQuest("Log transactions this week", 50)
    daily_quest_awarded = False
    weekly_quest_awarded = False

    player = PlayerProfile("You")
    player.load()

    coach = AICoach()

    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Account name: ")
            account_type = input("Type (savings/checking/credit): ")
            starting_balance = get_valid_number("Starting balance: ")

            if account_type == "savings":
                account = SavingsAccount(name, starting_balance)
            elif account_type == "checking":
                account = CheckingAccount(name, starting_balance)
            elif account_type == "credit":
                account = CreditAccount(name, starting_balance)
            else:
                print("Not a valid account type.")
                continue

            # → Account itself doesn't have save()/load() yet, this is a stopgap: write just enough of a row so account_id=1 actually
            #   exists in the database, which TransactionLedger.save() needs to satisfy the foreign key. Full Account persistence is a known limitation, documented in the README, not built tonight.
            conn = get_connection()
            conn.execute(
                "INSERT OR REPLACE INTO accounts (id, name, type, balance) VALUES (1, ?, ?, ?)",
                (name, account_type, starting_balance),
            )
            conn.commit()
            conn.close()

            ledger = TransactionLedger(account_id=1)
            ledger.load()  # → pull in any transactions saved from a previous session
            budget_engine = BudgetEngine(ledger)
            print(f"Created {account_type} account for {name}.")

        elif choice == "2":
            if account is None:
                print("Create an account first.")
                continue
            print(f"Balance: {account.get_balance()}")

        elif choice == "3":
            if account is None:
                print("Create an account first.")
                continue
            amount = get_valid_number("Deposit amount: ")
            account.deposit(amount)
            print("Deposited.")

        elif choice == "4":
            if account is None:
                print("Create an account first.")
                continue
            amount = get_valid_number("Withdraw amount: ")
            account.withdraw(amount)
            print("Withdrawn.")

        elif choice == "5":
            if ledger is None:
                print("Create an account first.")
                continue
            amount = get_valid_number("Transaction amount (negative for spending): ")
            category = input("Category: ")
            ledger.add_transaction(amount, category)
            ledger.save()  # → persist immediately, don't wait until exit
            print("Transaction logged.")

            # → check quest completion right after logging, this is the wiring that was missing, nothing triggered XP automatically before this
            if not daily_quest_awarded and daily_quest.check_completion(ledger):
                leveled_up = player.add_xp(daily_quest.get_reward())
                player.save()
                daily_quest_awarded = True
                summary = {
                    "event": "quest_completed",
                    "quest_name": daily_quest.name,
                    "xp_gained": daily_quest.get_reward(),
                }
                print(coach.narrate(summary))
                if leveled_up:
                    print(coach.narrate({"event": "level_up", "new_level": leveled_up}))

            if not weekly_quest_awarded and weekly_quest.check_completion(ledger):
                leveled_up = player.add_xp(weekly_quest.get_reward())
                player.save()
                weekly_quest_awarded = True
                summary = {
                    "event": "quest_completed",
                    "quest_name": weekly_quest.name,
                    "xp_gained": weekly_quest.get_reward(),
                }
                print(coach.narrate(summary))
                if leveled_up:
                    print(coach.narrate({"event": "level_up", "new_level": leveled_up}))

        elif choice == "6":
            if budget_engine is None:
                print("Create an account first.")
                continue
            print(budget_engine.get_summary())

        elif choice == "7":
            print(f"Level: {player.get_level()}  XP: {player.get_xp()}  Streak: {player.streak}")

        elif choice == "8":
            print(coach.narrate({"event": "status_check", "level": player.get_level()}))

        elif choice == "9":
            print("See you next time.")
            break

        else:
            print("Not a valid option, try again.")


if __name__ == "__main__":
    main()