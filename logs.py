import logging

# Konfiguracja loggera
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_info(message):
    # Logowanie informacji
    logging.info(message)

def log_warning(message):
    # Logowanie ostrzeżenia
    logging.warning(message)

def log_error(message):
    # Logowanie błędu
    logging.error(message)
