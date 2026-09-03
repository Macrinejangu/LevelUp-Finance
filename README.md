# LevelUp Finance

A gamified AI personal finance coach, built as a terminal application.

## Setup

1. python -m venv venv
2. Activate: source venv/bin/activate (Mac/Linux) or venv\Scripts\activate (Windows)
3. pip install -r requirements.txt
4. python main.py

## Project structure

- levelup/accounts.py, Account and subclasses
- levelup/ledger.py, TransactionLedger
- levelup/database.py, SQLite connection
- levelup/budget_engine.py, BudgetEngine
- levelup/quests.py, Quest and subclasses
- levelup/player_profile.py, PlayerProfile
- levelup/ai_coach.py, AICoach
- levelup/cli.py, menu and command routing
- schema.sql, database schema
- tests/, unit tests

## Commands

To be filled in as the CLI is built.

## Architecture

To be filled in, explain the separation between deterministic game logic and the AI narration layer.
