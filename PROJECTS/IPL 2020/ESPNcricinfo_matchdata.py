from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print("Driver initialized successfully")
    return driver

def scrape_ipl_2020_espncricinfo(url):
    driver = setup_driver()
    data = []
    
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print(f"Page title: {driver.title}")
        
        # Wait for match rows to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ds-p-4"))
        )
        match_containers = driver.find_elements(By.CLASS_NAME, "ds-p-4")
        print(f"Found {len(match_containers)} match containers")
        
        if not match_containers:
            print("No matches found. Saving page source for debugging.")
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            return data
        
        for match in match_containers:
            try:
                # Date
                date_elem = match.find_element(By.CLASS_NAME, "ds-text-compact-xs")
                date = date_elem.text.strip()  # e.g., "Sat, 19 Sep '20"
                
                # Teams
                team_elems = match.find_elements(By.CSS_SELECTOR, ".ci-team-score .ds-text-tight-m")
                teams = [team.text.strip() for team in team_elems if team.text.strip()]
                if len(teams) >= 2:
                    team1, team2 = teams[0], teams[1]
                else:
                    continue
                
                # Match Title
                match_title_elem = match.find_element(By.CSS_SELECTOR, ".ds-text-tight-s.ds-font-medium.ds-text-typo")
                match_title = match_title_elem.text.strip()  # e.g., "1st Match (N)"
                match_full = f"{team1} vs {team2}, {match_title}"
                
                # Result (Winner/Loser)
                result_elem = match.find_element(By.CSS_SELECTOR, ".ds-text-tight-s.ds-font-medium.ds-line-clamp-2")
                result = result_elem.text.strip()
                if "won" in result.lower():
                    if "tie" in result.lower():
                        winner, loser = "Tie", "Tie"
                    else:
                        winner = result.split(" won ")[0].strip()  # e.g., "CSK" or full team name
                        loser = team2 if winner in team1 else team1
                else:
                    winner, loser = "Tie", "Tie"
                
                # Place (Venue)
                venue_elem = match.find_element(By.XPATH, ".//div[contains(@class, 'ds-text-tight-s') and contains(@class, 'ds-font-regular')]")
                place = venue_elem.text.split("•")[1].split(",")[0].strip()  # e.g., "Abu Dhabi"
                
                # Store match data
                match_data = {
                    "date": date,
                    "match": match_full,
                    "winner": winner,
                    "loser": loser,
                    "place": place
                }
                print(f"Collected: {match_data}")
                data.append(match_data)
            except Exception as e:
                print(f"Error parsing match: {str(e)}")
                continue
        
        # Save to CSV
        csv_file = "ipl_2020_matches.csv"
        if data:
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                fieldnames = ["date", "match", "winner", "loser", "place"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"Data saved to {csv_file}")
        else:
            print("No data collected to write to CSV")
        
        return data
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return data
        
    finally:
        driver.quit()

url = "https://www.espncricinfo.com/series/ipl-2020-21-1210595/match-results"

if __name__ == "__main__":
    ipl_data = scrape_ipl_2020_espncricinfo(url)