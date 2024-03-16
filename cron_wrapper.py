"""Wrapper script for cron to clear blocked users.
app.py -> blocked.py -> here."""

import os
from dotenv import load_dotenv
from blocked import clear_blocked_users

def main():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=env_path)

    clear_blocked_users()

