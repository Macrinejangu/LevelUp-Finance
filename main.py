"""
Entry point for LevelUp Finance.
→ Run with: python main.py
"""
from levelup.cli import main
from levelup.database import init_db



if __name__ == "__main__":
  init_db()
  main()
    
