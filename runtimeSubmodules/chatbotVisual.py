"""Refactored chatbot visual functions for better modularity and readability."""

import time
import datetime

def typing_effect(text, delay=0.02):
    """Print text character-by-character to simulate chatbot typing."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def print_timestamp():
    """Return current time as HH:MM for chat message labels."""
    now = datetime.datetime.now()
    return now.strftime("%H:%M")
