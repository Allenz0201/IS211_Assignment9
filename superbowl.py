import requests
from bs4 import BeautifulSoup
import csv

URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_superbowl():
    response = requests.get(URL, headers=HEADERS)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table", class_="wikitable")
    if len(tables) < 2:
        print("No valid data tables found.")
        return

    table = tables[1]
    rows = table.find_all("tr")

    data = []
    for row in rows:
        cols = [col.get_text(strip=True) for col in row.find_all(["th", "td"])]
        if cols:
            data.append(cols)

    with open("superbowl_champions_clean.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    print(f" Scraped {len(data)-1} Super Bowls saved to superbowl_champions_clean.csv")

if __name__ == "__main__":
    scrape_superbowl()
