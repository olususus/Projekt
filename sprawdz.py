import os

def licz_linie_kodu(folder):
    total_linie = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.py'):  # Możesz zmienić rozszerzenie na inne, jeśli interesują cię inne pliki
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    linie = f.readlines()
                    total_linie += len(linie)
    return total_linie

if __name__ == "__main__":
    folder = input("Podaj ścieżkę do folderu: ")
    ilosc_linii = licz_linie_kodu(folder)
    print(f"Ilość linii kodu w folderze {folder}: {ilosc_linii}")
