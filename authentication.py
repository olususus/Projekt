class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class AuthenticationSystem:
    def __init__(self):
        self.users = []

    def register_user(self, username, password):
        new_user = User(username, password)
        self.users.append(new_user)
        print("Użytkownik zarejestrowany pomyślnie.")

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                print("Zalogowano pomyślnie.")
                return True
        print("Nieprawidłowy login lub hasło.")
        return False
