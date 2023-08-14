# Importujemy biblioteki
import requests
from bs4 import BeautifulSoup

# Wysyłamy żądanie GET do strony
url = "https://www.dailyfx.com/economic-calendar#today" # Podmień na prawdziwy adres strony
response = requests.get(url)

# Sprawdzamy, czy żądanie się powiodło
if response.status_code == 200:
    # Przekazujemy odpowiedź do obiektu BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Definiujemy funkcję, która sprawdza, czy tekst elementu jest równy "High"
    def is_high(element):
        return element.text == "High"

    # Wyszukujemy elementy, które spełniają warunek funkcji is_high
    elements = soup.find_all(is_high)

    print(soup)

    # Wyświetlamy znalezione elementy
    # for element in elements:
    #     print(element)
else:
    # Wyświetlamy błąd, jeśli żądanie się nie powiodło
    print(f"Błąd: {response.status_code}")
