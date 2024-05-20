# Zmiana importu z lokalnego pliku customer.py
from customer import Customer
from reservation import Reservation


class Room:
    def __init__(self, room_number, capacity, price_per_night, reserved=False):
        self.room_number = room_number
        self.capacity = capacity
        self.price_per_night = price_per_night
        self.reserved = reserved
        self.reservation = None

    def is_reserved(self):
        return self.reserved

    def reserve(self, customer, nights):
        if not self.reserved:
            self.reserved = True
            self.reservation = Reservation(customer, self, nights)
            return True
        else:
            return False

    def cancel_reservation(self):
        if self.reserved:
            self.reserved = False
            self.reservation = None
            return True
        else:
            return False

    def __str__(self):
        return f"Pokój {self.room_number} ({'Zajęty' if self.reserved else 'Dostępny'}), Cena za noc: {self.price_per_night} PLN"



class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def show_available_rooms(self):
        print(f"Dostępne pokoje w hotelu {self.name}:")
        available_rooms = [room for room in self.rooms if not room.is_reserved()]
        if available_rooms:
            for room in available_rooms:
                print(room)
        else:
            print("Brak dostępnych pokoi.")

    def reserve_room(self, room_number, customer, nights):
        for room in self.rooms:
            if room.room_number == room_number:
                if not room.is_reserved():
                    if room.reserve(customer, nights):
                        print(f"Pokój {room_number} został zarezerwowany przez {customer.name} na {nights} nocy.")
                    else:
                        print(f"Nie udało się zarezerwować pokoju {room_number}. Pokój jest już zajęty.")
                else:
                    print(f"Nie udało się zarezerwować pokoju {room_number}. Pokój jest już zajęty.")
                return
        print(f"Nie znaleziono pokoju o numerze {room_number}.")

    def cancel_reservation(self, room_number):
        for room in self.rooms:
            if room.room_number == room_number:
                if room.cancel_reservation():
                    print(f"Rezerwacja pokoju {room_number} została anulowana.")
                else:
                    print(f"Nie udało się anulować rezerwacji pokoju {room_number}. Pokój nie był zarezerwowany.")
                return
        print(f"Nie znaleziono pokoju o numerze {room_number}.")

    def show_my_reservations(self, customer):
        reservations = []
        for room in self.rooms:
            if room.reserved and room.reservation.customer == customer:
                reservations.append(room.reservation)

        if reservations:
            print(f"Aktualne rezerwacje użytkownika {customer.name}:")
            for reservation in reservations:
                print(f"Pokój {reservation.room.room_number}, Cena za noc: {reservation.room.price_per_night} PLN, Liczba nocy: {reservation.nights}, Łączna cena: {reservation.total_price()} PLN")
        else:
            print(f"Brak rezerwacji dla użytkownika {customer.name}.")

    def add_customer(self, name, email):
        customer = Customer(name, email)
        self.customers.append(customer)
        print(f"Klient {name} został dodany do systemu.")

    def find_customer_by_email(self, email):
        for customer in self.customers:
            if customer.email == email:
                return customer
        return None

    def generate_report(self):
        print(f"Raport dla hotelu {self.name}:")
        total_rooms = len(self.rooms)
        total_reserved = sum(1 for room in self.rooms if room.is_reserved())
        total_available = total_rooms - total_reserved
        print(f"Liczba wszystkich pokoi: {total_rooms}")
        print(f"Liczba zajętych pokoi: {total_reserved}")
        print(f"Liczba dostępnych pokoi: {total_available}")

        # Można dodać więcej statystyk, np. przychody z rezerwacji, najczęściej rezerwowane pokoje, itp.

    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.customers = []

        


