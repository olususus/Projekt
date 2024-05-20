class Customer:
    # Licznik dla identyfikatorów klientów
    customer_counter = 0

    def __init__(self, name, email):
        self.customer_id = Customer.generate_customer_id()  # Generujemy unikatowy identyfikator
        self.name = name
        self.email = email

    @classmethod
    def generate_customer_id(cls):
        # Inkrementujemy licznik i zwracamy wartość
        cls.customer_counter += 1
        return cls.customer_counter

    def __str__(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}, Email: {self.email}"


class CustomerManager:
    def __init__(self):
        self.customers = []

    def add_customer(self, name, email):
        customer = Customer(name, email)
        self.customers.append(customer)
        print(f"Klient {name} został dodany do bazy danych klientów.")

    def find_customer_by_email(self, email):
        for customer in self.customers:
            if customer.email == email:
                return customer
        return None

    def list_customers(self):
        if self.customers:
            print("Lista klientów:")
            for idx, customer in enumerate(self.customers, 1):
                print(f"{idx}. {customer}")
        else:
            print("Brak klientów w bazie danych.")

    def remove_customer(self, email):
        customer = self.find_customer_by_email(email)
        if customer:
            self.customers.remove(customer)
            print(f"Klient {customer.name} został usunięty z bazy danych klientów.")
        else:
            print("Nie znaleziono klienta o podanym adresie email.")

    def update_customer_email(self, email, new_email):
        customer = self.find_customer_by_email(email)
        if customer:
            customer.email = new_email
            print(f"Adres email klienta {customer.name} został zaktualizowany na {new_email}.")
        else:
            print("Nie znaleziono klienta o podanym adresie email.")
