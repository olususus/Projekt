import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY,
                    customer_id INTEGER,
                    start_date DATE,
                    end_date DATE,
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                )
            ''')
            self.connection.commit()
        except sqlite3.Error as e:
            print("Błąd podczas tworzenia tabel w bazie danych:", e)

    def add_customer(self, customer):
        try:
            self.cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (customer.name, customer.email))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print("Błąd podczas dodawania klienta do bazy danych:", e)
            return None

    def add_reservation(self, reservation):
        try:
            self.cursor.execute("INSERT INTO reservations (customer_id, start_date, end_date) VALUES (?, ?, ?)", (reservation.customer_id, reservation.start_date, reservation.end_date))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print("Błąd podczas dodawania rezerwacji do bazy danych:", e)
            return False

    def get_all_reservations(self):
        try:
            self.cursor.execute("SELECT * FROM reservations")
            reservations = self.cursor.fetchall()
            return reservations
        except sqlite3.Error as e:
            print("Błąd podczas pobierania rezerwacji z bazy danych:", e)
            return []

    def delete_reservation(self, reservation_id):
        try:
            self.cursor.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print("Błąd podczas usuwania rezerwacji:", e)
            return False
    
    def get_customer_reservations(self, customer_id):
        try:
            self.cursor.execute("SELECT * FROM reservations WHERE customer_id=?", (customer_id,))
            reservations = self.cursor.fetchall()
            return reservations
        except sqlite3.Error as e:
            print("Błąd podczas pobierania rezerwacji klienta:", e)
            return []
    
    def create_room_types_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS RoomTypes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price_per_night REAL NOT NULL
        );
        '''
        self.cursor.execute(query)
        self.connection.commit()
    
    def __del__(self):
        self.connection.close()
