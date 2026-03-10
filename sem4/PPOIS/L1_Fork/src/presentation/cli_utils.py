import re
import os
import time
from decimal import Decimal
from typing import List, TypeVar, Callable, Optional

T = TypeVar('T')


def get_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
            if min_val is not None and val < min_val:
                print(f"[Error] Number must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"[Error] Number must be at most {max_val}.")
                continue
            return val
        except ValueError:
            print("[Error] Please enter a valid integer.")

def get_decimal(prompt: str, min_val: float = 0.0) -> Decimal:
    while True:
        try:
            val = Decimal(input(prompt).strip())
            if val < Decimal(str(min_val)):
                print(f"[Error] Amount cannot be less than {min_val}.")
                continue
            return val
        except Exception:
            print("[Error] Please enter a valid decimal number (e.g., 5.00).")

def get_string(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("[Error] String cannot be empty.")

def get_name(prompt: str) -> str:
    while True:
        val = input(prompt).strip()
        if not val:
            print("[Error] Name cannot be empty.")
            continue
        if re.search(r'\d', val):
            print("[Error] Name cannot contain numbers.")
            continue
        return val

def select_item(items: List[T], label_func: Callable[[T], str], entity_name: str) -> Optional[T]:
    if not items:
        print(f"No available {entity_name}.")
        return None
        
    print(f"\nAvailable {entity_name}:")
    for i, item in enumerate(items, 1):
        print(f"{i}. {label_func(item)}")
    print("0. Cancel")
    
    choice = get_int(f"Select {entity_name} (0-{len(items)}): ", 0, len(items))
    if choice == 0:
        return None
    return items[choice - 1]


def clear_console() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def pause() -> None:
    """Hold the screen so the user can read output before returning to menu."""
    input("\nPress Enter to continue...")


def print_header(title: str) -> None:
    print(f"\n{'='*50}")
    print(f" {title.center(48)} ")
    print(f"{'='*50}")