import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# URL for IPL 2020 Points Table
url = "https://www.iplt20.com/points-table/men/2020"

# Set up Selenium with headless Chrome
options = Options()
options.headless = True  # Run without opening browser
driver = webdriver.Chrome(options=options)  # Requires chromedriver in PATH

# Fetch the page
print("Fetching IPL 2020 Points Table with Selenium...")
try:
    driver.get(url)
    time.sleep(3)  # Wait for JavaScript to load
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Find the points table
    table = soup.find("table", class_="ih-td-tab")
    if not table:
        print("Points table with class 'ih-td-tab' not found. Check class or URL.")
        driver.quit()
        exit()

    # Extract tbody with id="pointsdata"
    tbody = table.find("tbody", id="pointsdata")
    if not tbody:
        print("tbody with id='pointsdata' not found. Printing table content for debugging:")
        print(table.prettify()[:1000])  # Debug: Show table HTML
        driver.quit()
        exit()

    rows = tbody.find_all("tr")
    points_data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 10:  # Ensure enough columns
            team_div = cols[1].find("div", class_="ih-pt-ic")
            team = team_div.find("h2", class_="ih-pt-cont").text.strip() if team_div else "N/A"
            points_data.append({
                "Position": cols[0].text.strip(),
                "Team": team,
                "Played": int(cols[2].text.strip()),
                "Won": int(cols[3].text.strip()),
                "Lost": int(cols[4].text.strip()),
                "No Result": int(cols[5].text.strip()),
                "NRR": float(cols[6].text.strip()),
                "For": cols[7].text.strip(),
                "Against": cols[8].text.strip(),
                "Points": int(cols[9].text.strip()),
                "Recent Form": cols[10].text.strip() if len(cols) > 10 else "N/A"
            })

    # Save to CSV
    if points_data:
        df = pd.DataFrame(points_data)
        df.to_csv("ipl_2020_points_table.csv", index=False)
        print("Points Table saved to ipl_2020_points_table.csv")
        print(df.head())
    else:
        print("No data extracted from points table.")

except Exception as e:
    print(f"Error fetching {url}: {str(e)}")
finally:
    driver.quit()