import requests
from bs4 import BeautifulSoup

URL = "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_top_touchdowns(top_n=20):
    resp = requests.get(URL, headers=HEADERS)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the table containing player scoring/touchdowns
    # On the page there is a list under “Regular” / “Scoring” category.
    # We will find table rows and pick out player name, position, team, total TDs.
    table = soup.find("table", class_="TableBase-table")  # You may need to inspect exact class name
    if not table:
        print("Could not find the table on the page.")
        return

    rows = table.find_all("tr")[1:]  # skip header row

    print(f"{'Rank':<5} {'Player':<25} {'Pos':<4} {'Team':<5} {'TDs':>4}")
    count = 0
    for row in rows:
        if count >= top_n:
            break
        cols = row.find_all("td")
        if len(cols) < 5:
            continue
        rank = cols[0].get_text(strip=True)
        player = cols[1].get_text(strip=True)
        pos = cols[2].get_text(strip=True)
        team = cols[3].get_text(strip=True)
        tds = cols[4].get_text(strip=True)
        print(f"{rank:<5} {player:<25} {pos:<4} {team:<5} {tds:>4}")
        count += 1

if __name__ == "__main__":
    scrape_top_touchdowns(20)
