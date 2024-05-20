import datetime
import random
import string

import re

def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Nieprawidłowy adres email.")


def generate_confirmation_code():
    # Generowanie kodu potwierdzenia
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

def get_current_date():
    # Pobieranie bieżącej daty
    return datetime.date.today()

def calculate_age(birth_date):
    # Obliczanie wieku na podstawie daty urodzenia
    today = datetime.date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age
