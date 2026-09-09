# LevelUp Finance

A terminal-based personal finance tracker that turns real budgeting habits into an RPG. 
Log real transactions, stay on budget, and pay down real goals, and the app turns that into quests, XP, character levels, and long-term boss battles.
An AI coach, powered by a local Ollama model, narrates your progress in a witty, geeky voice, it never decides your score, it only describes what your real financial data already earned.

Built for the SDF-TFR18M3 Python CLI OOP assignment, Group 4.

## Setup

1. Clone the repository and move into the project folder.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it:
   - Mac/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Install [Ollama](https://ollama.com/download) separately, it's not a Python package, it's a background service that runs the AI mode locally.
6. Pull the model the app uses: `ollama pull phi4-mini`
7. Run the app: `python3 main.py`

The database file, `levelup_finance.db`, is created automatically the first time you run the app. It's excluded from Git on purpose, each person running this generates their own local copy.

## Usage

Run `python3 main.py` from the project root, not from inside the `levelup` folder. A menu appears with the following options:

1. **Create an account** — choose savings, checking, or credit, and set a starting balance.
2. **View balance** — shows the current balance on your active account.
3. **Deposit** — add money to your active account.
4. **Withdraw** — take money out, rejected if it exceeds your balance.
5. **Log a transaction** — record real spending or income, tied to a category.
   Use a negative amount for spending, positive for income.
6. **View budget summary** — see total spending, spending by category, and any categories currently over budget.
7. **View my profile** — see your current level, XP, and daily streak.
8. **Talk to my AI coach** — get a short, in-character message from the coach.
9. **Exit**

## Commands and input handling

All input is entered through the numbered menu, there are no separate CLI flags. Numeric fields (balances, amounts) reject non-numeric input and re-prompt rather than crashing.

## Architecture

The app is split into two layers that never mix.

**The finance layer** is the source of truth. `Account` and its subclasses (`SavingsAccount`, `CheckingAccount`, `CreditAccount`) handle balances and interest/fee logic. `TransactionLedger` records and persists every transaction to SQLite. `BudgetEngine` computes spending and budget status from real ledger data. `Quest` and its subclasses (`DailyQuest`, `WeeklyQuest`, `BossQuest`) check completion against that same real data. `PlayerProfile` tracks XP, level, and streak, all calculated deterministically.

**The AI layer** is `AICoach`. It never touches raw data, it only receives a small, already-computed summary dictionary, for example
`{"event": "quest_completed", "xp_gained": 25}`, and turns that into a sentence. It cannot see a ledger, an account, or a quest object directly, and it cannot influence XP, level, or quest completion. This separation is deliberate: if the AI could see raw data, someone could talk their way into free progress instead of earning it through real financial behavior. This is the project's main demonstration of **abstraction**.

**Persistence** uses SQLite (`schema.sql` defines the tables: `accounts`, `transactions`, `quests`, `player_profile`). `database.py` handles the connection and table creation. `PlayerProfile` and `TransactionLedger` each have their own `save()`/`load()` methods.

**Inheritance and polymorphism** show up in the `Account` hierarchy (each subclass calculates interest or fees differently) and the `Quest` hierarchy (each subclass checks completion differently, daily, weekly, or against a long-term target).

## Known limitations

A few things are documented here rather than fixed, in the interest of honesty about current scope:

- Quest completion and XP awarding aren't yet wired into the CLI menu. The underlying logic is built and tested (see `tests/`), but nothing in the menu currently triggers it automatically after logging a transaction.
- `Account` doesn't yet persist to the database, only `TransactionLedger` and `PlayerProfile` do. This means transactions can technically be logged before an account is formally saved.
- `BossQuest.get_progress()` currently sums all transactions in the ledger rather than filtering by a specific goal category, meaning two different boss battles could report identical progress.

## Tests

Run `pytest` from the project root. Test coverage includes `BudgetEngine`, `Quest` and its subclasses, and manual verification of `PlayerProfile`'s leveling and streak logic.