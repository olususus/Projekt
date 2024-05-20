class Config:
    # Dane do połączenia z bazą danych SQLite
    DATABASE_NAME = 'hotel.db'

    # Adresy e-mail do powiadomień
    ADMIN_EMAIL = 'admin@example.com'
    SUPPORT_EMAIL = 'support@example.com'

    # Ceny pokoi (w PLN za noc)
    SINGLE_ROOM_PRICE = 100
    DOUBLE_ROOM_PRICE = 150
    SUITE_PRICE = 250

    # Inne ustawienia aplikacji
    MAX_NIGHTS_PER_RESERVATION = 14  # Maksymalna liczba nocy na rezerwację
    MAX_ROOM_OCCUPANCY = 4  # Maksymalna liczba osób w pokoju
