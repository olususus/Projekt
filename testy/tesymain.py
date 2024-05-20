import tkinter as tk
from tkinter import messagebox

class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Reservation System")

        # Utwórz etykietę
        self.label = tk.Label(root, text="Witaj w systemie rezerwacji hotelowej", font=("Arial", 14))
        self.label.pack(pady=10)

        # Utwórz przyciski
        self.make_reservation_button = tk.Button(root, text="Zarezerwuj pokój", command=self.make_reservation)
        self.make_reservation_button.pack(pady=5)

        self.show_reservations_button = tk.Button(root, text="Wyświetl rezerwacje", command=self.show_reservations)
        self.show_reservations_button.pack(pady=5)

        self.exit_button = tk.Button(root, text="Wyjdź", command=root.quit)
        self.exit_button.pack(pady=5)

    def make_reservation(self):
        messagebox.showinfo("Zarezerwuj pokój", "Funkcja jeszcze nie zaimplementowana")

    def show_reservations(self):
        messagebox.showinfo("Wyświetl rezerwacje", "Funkcja jeszcze nie zaimplementowana")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()
