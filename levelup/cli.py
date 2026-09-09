"""
CLI menu and command routing.
→ Ties every module together into the terminal game loop.
→ Logging a transaction now checks daily/weekly quest completion and
  awards XP automatically, then the AI coach narrates it.
"""

from datetime import date

from levelup.database import (
    init_db,
    add_account,
    add_transaction,
    update_balance,
    get_all_accounts,
    get_transactions,
)
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
    account_id = None
    ledger = None
    budget_engine = None

    # Load the most recently saved account when the app starts.
    saved_accounts = get_all_accounts()

    if saved_accounts:
        saved_account = saved_accounts[-1]

        account_id = saved_account[0]
        name = saved_account[1]
        account_type = saved_account[2]
        balance = saved_account[3]

        if account_type == "savings":
            account = SavingsAccount(name, balance)
        elif account_type == "checking":
            account = CheckingAccount(name, balance)
        elif account_type == "credit":
            account = CreditAccount(name, balance)

        if account is not None:
            ledger = TransactionLedger(account_id)

            saved_transactions = get_transactions(account_id)

            for transaction in saved_transactions:
                ledger.transactions.append({
                    "id": transaction[0],
                    "account_id": transaction[1],
                    "amount": transaction[2],
                    "category": transaction[3],
                    "date": transaction[4],
                })

            budget_engine = BudgetEngine(ledger)

    # → standing quests for this session, checked every time a transaction gets logged.
    # Awarded flags are in-memory only, they reset if the app restarts.
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

            account_id = add_account(
                name,
                account_type,
                starting_balance
            )

            ledger = TransactionLedger(account_id)
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
            update_balance(account_id, account.get_balance())

            print("Deposited.")

        elif choice == "4":
            if account is None:
                print("Create an account first.")
                continue

            amount = get_valid_number("Withdraw amount: ")
            account.withdraw(amount)
            update_balance(account_id, account.get_balance())

            print("Withdrawn.")

        elif choice == "5":
            if ledger is None:
                print("Create an account first.")
                continue

            amount = get_valid_number(
                "Transaction amount (negative for spending): "
            )
            category = input("Category: ")

            ledger.add_transaction(amount, category)

            add_transaction(
                account_id,
                amount,
                category,
                date.today().isoformat()
            )

            print("Transaction logged.")

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
                    print(
                        coach.narrate(
                            {
                                "event": "level_up",
                                "new_level": leveled_up
                            }
                        )
                    )

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
                    print(
                        coach.narrate(
                            {
                                "event": "level_up",
                                "new_level": leveled_up
                            }
                        )
                    )

        elif choice == "6":
            if budget_engine is None:
                print("Create an account first.")
                continue

            print(budget_engine.get_summary())

        elif choice == "7":
            print(
                f"Level: {player.get_level()}  "
                f"XP: {player.get_xp()}  "
                f"Streak: {player.streak}"
            )

        elif choice == "8":
            print(
                coach.narrate(
                    {
                        "event": "status_check",
                        "level": player.get_level()
                    }
                )
            )

        elif choice == "9":
            print("See you next time.")
            break

        else:
            print("Not a valid option, try again.")


if __name__ == "__main__":
    main()