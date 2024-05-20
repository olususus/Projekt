import unittest
from customer import Customer
from reservation import Reservation
from hotel import Hotel

class TestHotelReservationSystem(unittest.TestCase):

    def setUp(self):
        self.customer1 = Customer("John Doe", "john@example.com")
        self.customer2 = Customer("Jane Smith", "jane@example.com")
        self.hotel = Hotel("Sample Hotel")

    def test_customer_creation(self):
        self.assertEqual(self.customer1.name, "John Doe")
        self.assertEqual(self.customer1.email, "john@example.com")

    def test_reservation_creation(self):
        reservation = Reservation(self.customer1, 101, 3)
        self.assertEqual(reservation.customer, self.customer1)
        self.assertEqual(reservation.room_number, 101)
        self.assertEqual(reservation.nights, 3)

    def test_hotel_creation(self):
        self.assertEqual(self.hotel.name, "Sample Hotel")

    def test_hotel_add_customer(self):
        self.hotel.add_customer("Alice Johnson", "alice@example.com")
        self.assertEqual(len(self.hotel.customers), 1)

    def test_hotel_reserve_room(self):
        self.hotel.add_customer("Alice Johnson", "alice@example.com")
        self.hotel.add_customer("Bob Brown", "bob@example.com")
        self.hotel.add_room(101, 2, 150)
        self.hotel.add_room(102, 4, 200)
        self.hotel.reserve_room(101, self.hotel.customers[0], 2)
        self.assertTrue(self.hotel.rooms[0].is_reserved())

if __name__ == '__main__':
    unittest.main()
