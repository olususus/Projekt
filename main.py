import customtkinter as ctk
from customtkinter import E, END, N, NO, NS, ON, S, W, X, Y
from tkinter import *
from tkinter import messagebox, simpledialog, filedialog
from database import Database
from reservation import Reservation
from customer import Customer
from utils import validate_email
import pygame
import cv2
from time import sleep
import requests
from tkinter import messagebox, simpledialog
import gmplot
import folium
import webbrowser
from gtfs import read_gtfs_file
import csv
from functools import lru_cache
import calendar
import tkinter as tk
import sys
from PIL import Image, ImageTk
import random

def play_buzzer(filepath):
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

def play_yay(filepath):
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

def play_intro(filepath):
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.loop.play()

def play_waiting_music(filepath):
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()

class WeatherApp:

    def __init__(self, master):
        self.master = master
        master.title('Weather Information')
        self.label_city = ctk.CTkLabel(master, text='Wprowad miasto:')
        self.label_city.pack()
        self.entry_city = ctk.CTkEntry(master)
        self.entry_city.pack()
        self.button_get_weather = ctk.CTkButton(master, text='Pobierz Pogod', command=self.get_weather)
        self.button_get_weather.pack()
        self.label_weather_info = ctk.CTkLabel(master, text='')
        self.label_weather_info.pack()

    def get_weather(self):
        city = self.entry_city.get()
        if city:
            try:
                url = f'https://www.metaweather.com/api/location/search/?query={city}'
                response = requests.get(url)
                data = response.json()
                if data and len(data) > 0:
                    woeid = data[0]['woeid']
                    url = f'https://www.metaweather.com/api/location/{woeid}/'
                    response = requests.get(url)
                    data = response.json()
                    if data and 'consolidated_weather' in data:
                        consolidated_weather = data['consolidated_weather']
                        if consolidated_weather and len(consolidated_weather) > 0:
                            weather_today = consolidated_weather[0]
                            temperature = round(weather_today['the_temp'], 2)
                            weather_state = weather_today['weather_state_name']
                            weather_info = f'Temperatura: {temperature}C\nStan pogody: {weather_state}'
                            self.label_weather_info.configure(text=weather_info)
                        else:
                            messagebox.showwarning('Ostrzeenie', 'Brak danych pogodowych dla podanego miasta.')
                    else:
                        messagebox.showwarning('Ostrzeenie', 'Brak danych pogodowych dla podanego miasta.')
                else:
                    messagebox.showwarning('Ostrzeenie', 'Nie znaleziono podanego miasta.')
            except Exception as e:
                messagebox.showerror('Bd', f'Wystpi bd: {str(e)}')
        else:
            messagebox.showerror('Bd', 'Prosz wprowadzi nazw miasta.')

class StartScreen:

    def __init__(self, master):
        self.master = master
        master.title('Hotel Reservation System')
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
        pygame.display.set_caption('Start Screen')
        self.movie = ''
        self.cap = cv2.VideoCapture(self.movie)
        self.frame_rate = int(self.cap.get(cv2.CAP_PROP_FPS))
        pygame.mixer.quit()
        self.clock = pygame.time.Clock()

    def play_movie(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], 'RGB')
            self.screen.blit(frame, (0, 0))
            pygame.display.flip()
            self.clock.tick(self.frame_rate)
        self.cap.release()
        pygame.quit()
        self.show_main_interface()

    def show_main_interface(self):
        root = ctk.CTk()
        app = HotelApp(root)
        root.mainloop()

class HotelApp:

    def __init__(self, master):
        self.master = master
        master.title('Hotel Connection')
        self.db = Database('hotel.db')
        self.db.create_tables()
        self.witamy = ctk.CTkLabel(master, text='Witaj!')
        self.witamy.grid(row=1, column=0, columnspan=2)
        self.rezerwacyje = ctk.CTkButton(master, text='Zarezerwuj', command=lambda: [self.zarezerwoj()])
        self.rezerwacyje.grid(row=2, column=0, columnspan=2)
        self.additional_features_button = ctk.CTkButton(master, text='Dodatkowe Funkcje', command=lambda: [self.open_additional_features()])
        self.additional_features_button.grid(row=3, column=0, columnspan=2)
        self.button_explore = ctk.CTkButton(master, text='Zwiedzanie', command=lambda: [self.explore_places()])
        self.button_explore.grid(row=4, column=0, columnspan=2)
        self.button_infolinia = ctk.CTkButton(master, text='Infolinia', command=lambda: [self.infolinia()])
        self.button_infolinia.grid(row=5, column=0, columnspan=2)
        self.exit_button = ctk.CTkButton(master, text='Wyjdz', command=lambda: [self.destrukcja()])
        self.information_button = ctk.CTkButton(master, text='Twórca', command=lambda: [messagebox.showinfo(message=('Tylko ja'))])
        self.reklama_troll_button = ctk.CTkButton(master, text='Info', command=lambda: [self.info_trollig()])
        self.reklama_troll_button.grid(row=8, column=0, columnspan=2)
        self.information_button.grid(row=6, column=0, columnspan=2)
        self.exit_button.grid(row=7, column=0, columnspan=2)
        self.dla_gosci = ctk.CTkButton(master, text='Dla Gosci Hotelu', command=lambda: [self.system_gosci()])
        self.dla_gosci.grid(row=9, column=0, columnspan=2)

    def system_gosci(self):
        goscie = ctk.CTkToplevel(self.master)
        goscie.title('Goscie Hotelu')
        self.guzik_goscie_info = ctk.CTkButton(goscie, text='Informacja dla gosci.', command= lambda:[messagebox.showinfo(message='Dzisiejszy obiad odbywa sie tylko na 1 i 2 pietrze ze wzgledu na wesele w restauracji na 1 pietrze.')])
        self.guzik_goscie_info.pack()
        self.guzik_roomservice = ctk.CTkButton(goscie, text='Room Service', command=lambda:[messagebox.showinfo(message='Room Service pojawi sie w pana pokoju w nastepstwie nastepnych 5 minut')])
        self.guzik_roomservice.pack()
        self.againadmin = ctk.CTkButton(goscie, text='Admin all over again', command =lambda:[self.admin_mode()])
        self.againadmin.pack()

    def info_trollig(self):
        pygame.mixer.init()
        pygame.mixer.music.load('ads.mp3')
        pygame.mixer.music.play()
        messagebox.showinfo(message='Ten program jest sponsorowany przez RAID SHADOW LEGENDS!')

    def destrukcja(self):
        pygame.mixer.init()
        pygame.mixer.music.load('fart.mp3')
        pygame.mixer.music.play()
        sleep(6)
        sys.exit()

    def infolinia(self):
        infoliniowanie = ctk.CTkToplevel(self.master)
        infoliniowanie.title('Infolinia')
        w_kolejce = random.randint(1,1987)
        self.button_infolinia1 = ctk.CTkButton(infoliniowanie, text='Zadzwon Na Infolinie', command= lambda: [play_waiting_music('patience.mp3'), messagebox.showinfo(message=('Witaj na Infolinii!')), messagebox.showinfo(title=('Kolejka:'), message=f'Jesteś {w_kolejce} W kolejce!'), messagebox.showinfo(message=('Łączenie z pracownikiem infolini...')), messagebox.showinfo(message=('Pracownik Infolinii: Witaj na Infolinii. Chciałem tylko ogłosić że...')), messagebox.showwarning(message=('W tej infolinii zrobisz absolutne NIC!')), messagebox.showerror(message=('Jedyne co tu zrobisz to pogadasz z irytujacym pracownikiem')), messagebox.showerror(message=('Miłego Dnia.'))])
        self.button_infolinia1.grid(row=0, column=0, columnspan=2)

    def zarezerwoj(self):
        rezerwowanie = ctk.CTkToplevel(self.master)
        rezerwowanie.title('Rezerwacja')
        self.label_name = ctk.CTkLabel(rezerwowanie, text='Pełne Imię: ')
        self.label_name.grid(row=0, column=0, columnspan=2)
        self.label_email = ctk.CTkLabel(rezerwowanie, text='Email: ')
        self.label_email.grid(row=1, column=0, columnspan=2)
        self.label_start_date = ctk.CTkLabel(rezerwowanie, text='Początek: ')
        self.label_start_date.grid(row=2, column=0, columnspan=2)
        self.label_end_date = ctk.CTkLabel(rezerwowanie, text='Koniec: ')
        self.label_end_date.grid(row=3, column=0, columnspan=2)
        self.entry_name = ctk.CTkEntry(rezerwowanie)
        self.entry_name.grid(row=0, column=1, columnspan=2)
        self.entry_email = ctk.CTkEntry(rezerwowanie)
        self.entry_email.grid(row=1, column=1, columnspan=2)
        self.entry_start_date = ctk.CTkEntry(rezerwowanie)
        self.entry_start_date.grid(row=2, column=1, columnspan=2)
        self.entry_end_date = ctk.CTkEntry(rezerwowanie)
        self.entry_end_date.grid(row=3, column=1, columnspan=2)
        self.submit_button = ctk.CTkButton(rezerwowanie, text='Zarezerwuj', command=self.submit_reservation)
        self.submit_button.grid(row=4, column=0, columnspan=2)

    def explore_places(self):
        location = simpledialog.askstring('Zwiedzanie', 'Podaj lokalizacj:')
        if location:
            try:
                url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=popularne+miejsca+w+{location}&key=AIzaSyA_NiZBwDqs0mV32KBDe_pNem23aVOad5U'
                response = requests.get(url)
                data = response.json()
                if 'results' in data:
                    results = data['results']
                    places_list = '\n'.join([result['name'] for result in results])
                    messagebox.showinfo('Popularne miejsca', f'Popularne miejsca w {location}:\n{places_list}')
                    play_yay('yay.mp3')
                else:
                    messagebox.showwarning('Ostrzeenie', 'Brak danych o popularnych miejscach.')
                    play_buzzer('buzzer.mp3')
            except Exception as e:
                messagebox.showerror('Bd', f'Wystpi bd: {str(e)}')
                play_buzzer('buzzer.mp3')
        else:
            messagebox.showerror('Bd', 'Prosz wprowadzi lokalizacj.')
            play_buzzer('buzzer.mp3')

    def submit_reservation(self):
        customer_name = self.entry_name.get()
        customer_email = self.entry_email.get()
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()
        if customer_name and customer_email and start_date and end_date:
            try:
                validate_email(customer_email)
                customer = Customer(customer_name, customer_email)
                customer_id = self.db.add_customer(customer)
                if customer_id is not None:
                    reservation = Reservation(customer_id, start_date, end_date)
                    if self.db.add_reservation(reservation):
                        messagebox.showinfo('Sukces', 'Rezerwacja zostaa dodana.')
                        play_yay('yay.mp3')
                    else:
                        messagebox.showerror('Bd', 'Wystpi bd podczas dodawania rezerwacji.')
                        play_buzzer('buzzer.mp3')
                else:
                    messagebox.showerror('Bd', 'Wystapil blad podczas dodawania klienta.')
                    play_buzzer('buzzer.mp3')
            except ValueError as e:
                messagebox.showerror('Bd', str(e))
                play_buzzer('buzzer.mp3')
        else:
            messagebox.showerror('Bd', 'Prosze uzupelnij wszystkie pola.')
            play_buzzer('buzzer.mp3')

    def open_additional_features(self):
        additional_features_window = ctk.CTkToplevel(self.master)
        additional_features_window.title('Dodatkowe Funkcje')
        admin_mode_button = ctk.CTkButton(additional_features_window, text='Admin Mode', command=self.admin_mode)
        admin_mode_button.pack()
        children_module_button = ctk.CTkButton(additional_features_window, text='Modu dla dzieci', command=self.open_children_module)
        children_module_button.pack()
        events_button = ctk.CTkButton(additional_features_window, text='Wydarzenia w okolicy', command=self.display_nearby_events)
        events_button.pack()
        restaurant_button = ctk.CTkButton(additional_features_window, text='Znajdz Restauracje', command=self.find_nearby_restaurants)
        restaurant_button.pack()
        calendar_button = ctk.CTkButton(additional_features_window, text='Kalendarz', command=self.calendarapp)
        calendar_button.pack()

        def open_map():
            warsaw_map = folium.Map(location=[52.2297, 21.0122], zoom_start=12)
            points_of_interest = [{'name': 'Stare Miasto', 'location': [52.2503, 21.0125]}, {'name': 'azienki Krlewskie', 'location': [52.2159, 21.0355]}, {'name': 'Paac Kultury i Nauki', 'location': [52.2315, 21.0067]}, {'name': 'Muzeum Powstania Warszawskiego', 'location': [52.2322, 20.9811]}, {'name': 'Ogrd Saski', 'location': [52.240303, 21.007661]}, {'name': 'Centrum Nauki Kopernik', 'location': [52.24193, 21.028512]}, {'name': 'Dom Twrcy', 'location': [52.282009, 21.061219]}]
            for point in points_of_interest:
                folium.Marker(location=point['location'], popup=point['name']).add_to(warsaw_map)
            warsaw_map.save('warsaw_map.html')
            webbrowser.open('warsaw_map.html')
        map_button = ctk.CTkButton(additional_features_window, text='Zwiedzanie Warszawy', command=open_map)
        map_button.pack()

    def display_nearby_events(self):
        nearby_events_window = ctk.CTkToplevel(self.master)
        nearby_events_window.title('Wydarzenia w okolicy')
        latitude = 52.22854757598444
        longitude = 20.9951219230219
        api_key = 'AIzaSyA_NiZBwDqs0mV32KBDe_pNem23aVOad5U'
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=1000&type=event&key={api_key}'
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                for event in data['results']:
                    name = event['name']
                    address = event['vicinity']
                    event_label = ctk.CTkLabel(nearby_events_window, text=f'Wydarzenie: {name}, Adres: {address}')
                    event_label.pack()
            else:
                error_label = ctk.CTkLabel(nearby_events_window, text=f'Bd: {response.status_code}')
                error_label.pack()
                play_buzzer('buzzer.mp3')
        except Exception as e:
            error_label = ctk.CTkLabel(nearby_events_window, text=f'Bd podczas pobierania danych: {str(e)}')
            error_label.pack()
            play_buzzer('buzzer.mp3')

    def find_directionsnotworking1(self):
        location = simpledialog.askstring('Znajd dojazd', 'Podaj miejsce, do ktrego chcesz dojecha:')
        if location:
            try:
                url = f'https://www.google.com/maps/dir/?api=AIzaSyA_NiZBwDqs0mV32KBDe_pNem23aVOad5U&destination={location}'
                webbrowser.open(url)
                play_yay('yay.mp3')
            except Exception as e:
                messagebox.showerror('Bd', f'Wystpi bd: {str(e)}')
                play_buzzer('buzzer.mp3')
        else:
            messagebox.showerror('Bd', 'Prosz wprowadzi miejsce docelowe.')
            play_buzzer('buzzer.mp3')

    def calendarapp(self):
        kalendarz = ctk.CTkToplevel(self.master)
        kalendarz.title('Kalendarz')
        self.cal = calendar.TextCalendar(calendar.SUNDAY)
        self.year = tk.StringVar()
        self.month = tk.StringVar()
        self.year_label = ctk.CTkLabel(kalendarz, text='Rok:')
        self.year_label.grid(row=0, column=0)
        self.year_entry = ctk.CTkEntry(kalendarz, textvariable=self.year)
        self.year_entry.grid(row=0, column=1)
        self.month_label = ctk.CTkLabel(kalendarz, text='Miesic:')
        self.month_label.grid(row=0, column=2)
        self.month_entry = ctk.CTkEntry(kalendarz, textvariable=self.month)
        self.month_entry.grid(row=0, column=3)
        self.show_button = ctk.CTkButton(kalendarz, text='Poka kalendarz', command=self.show_calendar)
        self.show_button.grid(row=0, column=4)
        self.calendar_display = ctk.CTkTextbox(kalendarz, height=10, width=25)
        self.calendar_display.grid(row=1, columnspan=5)

    def show_calendar(self):
        year = int(self.year.get())
        month = int(self.month.get())
        cal_output = self.cal.formatmonth(year, month)
        self.calendar_display.delete(1.0, tk.END)
        self.calendar_display.insert(tk.END, cal_output)

    def find_nearby_restaurants(self):
        location = simpledialog.askstring('Znajd Restauracje', 'Podaj lokalizacj (miasto, ulica, itp.):')
        if location:
            try:
                url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query=restaurants+in+{location}&key=AIzaSyA_NiZBwDqs0mV32KBDe_pNem23aVOad5U'
                response = requests.get(url)
                data = response.json()
                if 'results' in data:
                    restaurants = [res['name'] for res in data['results']]
                    if restaurants:
                        messagebox.showinfo(f'Restauracje w Okolicy {location}', '\n'.join(restaurants))
                        play_yay('yay.mp3')
                    else:
                        messagebox.showinfo('Restauracje w Okolicy', 'Brak restauracji w pobliu.')
                        play_buzzer('buzzer.mp3')
                else:
                    messagebox.showerror('Bd', 'Brak danych o restauracjach.')
                    play_buzzer('buzzer.mp3')
            except Exception as e:
                messagebox.showerror('Bd', f'Wystpi bd: {str(e)}')
                play_buzzer('buzzer.mp3')
        else:
            messagebox.showerror('Bd', 'Prosz wprowadzi lokalizacj.')
            play_buzzer('buzzer.mp3')

    def admin_mode(self):
        password = simpledialog.askstring('Admin Mode', 'Podaj haso:')
        if password == '123123':
            admin_window = ctk.CTkToplevel(self.master)
            admin_window.title('Tryb admina')
            all_reservations = self.db.get_all_reservations()
            for idx, reservation in enumerate(all_reservations, start=1):
                reservation_info = f'ID: {reservation[0]}, Customer ID: {reservation[1]}, Start Date: {reservation[2]}, End Date: {reservation[3]}'
                ctk.CTkLabel(admin_window, text=reservation_info).grid(row=idx, column=0, sticky=W)
            export_button = ctk.CTkButton(admin_window, text='Eksportuj dane', command=self.export_data)
            export_button.grid(row=len(all_reservations) + 1, column=0, columnspan=2)
            delete_button = ctk.CTkButton(admin_window, text='Usu rezerwacj', command=self.delete_reservation)
            delete_button.grid(row=len(all_reservations) + 2, column=0, columnspan=2)
        else:
            messagebox.showerror('Bd', 'Nieprawidowe haso.')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')
            play_buzzer('buzzer.mp3')

    def open_children_module(self):
        children_module_window = ctk.CTkToplevel(self.master)
        children_module_window.title('Modu dla dzieci')
        button_image = ctk.CTkImage(Image.open("afton.png"), size=(26, 26))
        playground_button = ctk.CTkButton(children_module_window, text='Bawialnia', command=self.playground)
        playground_button.pack()
        pool_button = ctk.CTkButton(children_module_window, text='Brodzik', command=self.pool)
        pool_button.pack()

    def playground(self):
        messagebox.showinfo('Bawialnia', "W Bawialni dla dzieci: 'Dzieci w Kulkach' znajduj si:\n- Zabawki\n- Kulki\n- Telewizor z bajkami\n- Konsola XBOX oraz PLAYSTATION\n- Duy wybr pyt CD.")

    def pool(self):
        messagebox.showinfo('Brodzik', "W Brodziku: 'Woda z Dziecmi; znajduje si:\n- Woda w temperaturze pokojowej\n- Zjedzalnia\n- Zabawki wodne\n- Pistolety wodne.")

    def delete_reservation(self):
        reservation_id = simpledialog.askinteger('Usu rezerwacj', 'Podaj ID rezerwacji do usunicia:')
        if reservation_id:
            if self.db.delete_reservation(reservation_id):
                messagebox.showinfo('Sukces', 'Rezerwacja zostaa usunita.')
            else:
                messagebox.showerror('Bd', 'Bd podczas usuwania rezerwacji.')
        else:
            messagebox.showerror('Bd', 'Nieprawidowe ID rezerwacji.')

    def export_data(self):
        file_name = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt')])
        if file_name:
            all_reservations = self.db.get_all_reservations()
            with open(file_name, 'w') as file:
                for reservation in all_reservations:
                    file.write(f'ID: {reservation[0]}, Customer ID: {reservation[1]}, Start Date: {reservation[2]}, End Date: {reservation[3]}\n')
            messagebox.showinfo('Sukces', 'Dane zostay pomylnie wyeksportowane do pliku.')

def main():
    root = ctk.CTk()
    app = StartScreen(root)
    app.play_movie()
    root.mainloop()
if __name__ == '__main__':
    main()
