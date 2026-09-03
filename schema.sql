-- LevelUp Finance, database schema
-- Agreed as a team, Sprint 1, Day 1

-- accounts
-- Backs the Account class and its subclasses
-- (SavingsAccount, CheckingAccount, CreditAccount)

CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('savings', 'checking', 'credit')),
    balance REAL NOT NULL DEFAULT 0
);

-- transactions
-- Backs the TransactionLedger class
-- amount is signed: positive = deposit, negative = withdrawal
-- This keeps category totals and budget math a simple sum, no branching needed.

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- quests
-- Backs Quest and its subclasses (DailyQuest, WeeklyQuest, BossQuest)
-- One table for all three types.
-- target_amount and current_progress are only used by BossQuest,
-- they stay NULL for Daily and Weekly quests.

CREATE TABLE quests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quest_type TEXT NOT NULL CHECK (quest_type IN ('daily', 'weekly', 'boss')),
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed')),
    reward_xp INTEGER NOT NULL,
    target_amount REAL,
    current_progress REAL,
    created_date TEXT NOT NULL,
    completed_date TEXT
);


-- player_profile
-- Backs the PlayerProfile class
-- Single-row table, this is a one-user app, not multi-player.

CREATE TABLE player_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    xp INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 1,
    streak INTEGER NOT NULL DEFAULT 0,
    last_active_date TEXT
);

-- Seed the single player row so the app always has one to read from.
INSERT INTO player_profile (id, xp, level, streak) VALUES (1, 0, 1, 0);
