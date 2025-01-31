import time
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()  # Installs the appropriate version
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json

def scrape_flights(departure, destination, date):
    url = f"https://www.google.com/travel/flights?q=flights+from+{departure}+to+{destination}+on+{date}"
    
    options = uc.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    flights = []
    for flight in soup.find_all("div", class_="pIav2d"):
        try:
            airline = flight.find("div", class_="sSHqwe tPgKwe ogfYpf").text
            price = flight.find("div", class_="YMlIz FpEdX").text
            link = flight.find("a")["href"]  # Extracts the booking link

            full_link = f"https://www.google.com{link}"  # Ensure full URL
            flights.append({"airline": airline, "price": price, "link": full_link})
        except:
            continue

    return flights

if __name__ == "__main__":
    flights = scrape_flights("New York", "Los Angeles", "2025-02-15")
    print(json.dumps(flights))