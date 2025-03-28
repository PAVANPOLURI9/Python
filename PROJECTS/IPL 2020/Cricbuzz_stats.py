from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import os
import glob

# --------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------
MATCHES_URL = "https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/matches"
STATS_URL = "https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/stats"
OUTPUT_MATCH_CSV = "ipl_2020_match_data.csv"
OUTPUT_STATS_CSV = "ipl_2020_all_stats.csv"
FINAL_CSV = "ipl_2020_combined_data.csv"
DELETE_INDIVIDUAL_CSVS = True  # Set to False if you want to keep individual CSVs

# --------------------------------------------------------------------
# Driver Setup
# --------------------------------------------------------------------
def setup_driver():
    """Setup Edge WebDriver with anti-automation options"""
    try:
        options = webdriver.EdgeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0"
        })
        return driver
    except Exception as e:
        print(f"Driver setup failed: {e}")
        return None

# --------------------------------------------------------------------
# Overlay Handling
# --------------------------------------------------------------------
def handle_overlays(driver):
    """Handle popups or overlays that might block clicks"""
    try:
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), ' Agree')]"))
        )
        cookie_button.click()
        print("Closed cookie popup")
    except:
        pass  # No overlay found

# --------------------------------------------------------------------
# Match Scraping Functions
# --------------------------------------------------------------------
def get_all_match_urls(driver, main_url):
    """Fetch all match URLs from the matches page"""
    driver.get(main_url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    match_links = []
    for tag in soup.select("a.text-hvr-underline"):
        href = tag.get("href", "")
        if "/live-cricket-scores/" in href or "/cricket-scores/" in href:
            full_link = "https://www.cricbuzz.com" + href
            if full_link not in match_links:
                match_links.append(full_link)
    return match_links

def scrape_match_details(driver, match_url):
    """Scrape match details from a match page"""
    driver.get(match_url)
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    data = {
        "match_url": match_url,
        "match_title": soup.find("h1", class_="cb-nav-hdr").get_text(strip=True) if soup.find("h1", class_="cb-nav-hdr") else "",
        "match_subhdr": soup.find("div", class_="cb-nav-subhdr").get_text(" ", strip=True) if soup.find("div", class_="cb-nav-subhdr") else "",
        "match_status": "",
        "commentary": ""
    }
    
    status_tag = soup.find("div", class_="cb-text-complete") or soup.find("div", class_="cb-text-live") or soup.find("div", class_="cb-text-inprogress")
    data["match_status"] = status_tag.get_text(strip=True) if status_tag else ""
    
    commentary_texts = [comm.get_text(strip=True) for comm in soup.find_all("p", class_="cb-com-ln") if comm.get_text(strip=True)]
    data["commentary"] = "\n".join(commentary_texts)
    
    return data

# --------------------------------------------------------------------
# Stats Scraping Functions
# --------------------------------------------------------------------
def scrape_stats_table(driver, wait, category, stat_type):
    """Scrape stats table for a given category (batting or bowling)"""
    try:
        print(f"Scraping {category} stats ({stat_type})...")
        table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table.cb-series-stats")))
        
        headers = [th.text.strip() for th in table.find_elements(By.CSS_SELECTOR, "thead th")]
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
        data = []
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= len(headers):
                row_data = {headers[i]: cols[i].text.strip() for i in range(len(headers))}
                player_key = 'Batter' if stat_type == 'Batting' else 'Bowler'
                row_data[player_key] = cols[1].find_element(By.TAG_NAME, "a").text.strip() if cols[1].find_elements(By.TAG_NAME, "a") else cols[1].text.strip()
                row_data['Category'] = category
                row_data['Stat_Type'] = stat_type
                data.append(row_data)
        
        return pd.DataFrame(data) if data else None
    except Exception as e:
        print(f"Error scraping {category} stats: {e}")
        return None

def scrape_all_stats_categories(driver, wait, base_url):
    """Scrape all batting and bowling stat categories"""
    categories = {
        "Most Runs": {"tab_id": "mostRuns", "type": "Batting"},
        "Highest Scores": {"tab_id": "highestScore", "type": "Batting"},
        "Best Batting Average": {"tab_id": "highestAvg", "type": "Batting"},
        "Best Batting Strike Rate": {"tab_id": "highestSr", "type": "Batting"},
        "Most Hundreds": {"tab_id": "mostHundreds", "type": "Batting"},
        "Most Fifties": {"tab_id": "mostFifties", "type": "Batting"},
        "Most Fours": {"tab_id": "mostFours", "type": "Batting"},
        "Most Sixes": {"tab_id": "mostSixes", "type": "Batting"},
        "Most Nineties": {"tab_id": "mostNineties", "type": "Batting"},
        "Most Wickets": {"tab_id": "mostWickets", "type": "Bowling"},
        "Best Bowling Average": {"tab_id": "lowestAvg", "type": "Bowling"},
        "Best Bowling": {"tab_id": "bestBowlingInnings", "type": "Bowling"},
        "Most 5 Wickets Haul": {"tab_id": "mostFiveWickets", "type": "Bowling"},
        "Best Economy": {"tab_id": "lowestEcon", "type": "Bowling"},
        "Best Bowling Strike Rate": {"tab_id": "lowestSr", "type": "Bowling"}
    }
    
    driver.get(base_url)
    time.sleep(5)
    handle_overlays(driver)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cb-stats-lft-ancr")))
    
    all_dataframes = []
    for category, info in categories.items():
        try:
            link = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@ng-click=\"setTab('{info['tab_id']}')\"]")))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", link)
            time.sleep(3)
            
            df = scrape_stats_table(driver, wait, category, info['type'])
            if df is not None:
                all_dataframes.append(df)
                print(f"✅ Scraped {category} ({info['type']})")
        except Exception as e:
            print(f"Error processing {category}: {e}")
    
    return pd.concat(all_dataframes, ignore_index=True, sort=False) if all_dataframes else None

# --------------------------------------------------------------------
# Merge CSV Files
# --------------------------------------------------------------------
def merge_csv_files(output_files, final_csv, delete_individual=False):
    """Merge all CSV files into one and optionally delete the originals"""
    try:
        # Read all CSV files into a list of DataFrames
        dfs = [pd.read_csv(file) for file in output_files if os.path.exists(file)]
        if not dfs:
            print("No CSV files to merge!")
            return
        
        # Concatenate all DataFrames, handling differing columns
        combined_df = pd.concat(dfs, ignore_index=True, sort=False)
        combined_df.to_csv(final_csv, index=False)
        print(f"✅ Merged all CSV files into {final_csv}")
        print(f"Total rows in combined file: {len(combined_df)}")
        
        # Delete individual CSV files if specified
        if delete_individual:
            for file in output_files:
                os.remove(file)
                print(f"Deleted individual file: {file}")
    except Exception as e:
        print(f"Error merging CSV files: {e}")

# --------------------------------------------------------------------
# Main Function
# --------------------------------------------------------------------
def main():
    """Main function to run the scraper and merge CSVs"""
    driver = setup_driver()
    if not driver:
        return
    
    wait = WebDriverWait(driver, 20)
    output_files = []  # Track all generated CSV files
    
    try:
        # Scrape match data
        print("Fetching all match URLs for IPL 2020...")
        match_urls = get_all_match_urls(driver, MATCHES_URL)
        print(f"Total match URLs found: {len(match_urls)}")
        
        if match_urls:
            with open(OUTPUT_MATCH_CSV, mode="w", newline="", encoding="utf-8") as f:
                fieldnames = ["match_url", "match_title", "match_subhdr", "match_status", "commentary"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for idx, url in enumerate(match_urls, start=1):
                    print(f"Scraping match {idx}/{len(match_urls)} => {url}")
                    try:
                        match_data = scrape_match_details(driver, url)
                        writer.writerow(match_data)
                    except Exception as e:
                        print(f"Error scraping {url}: {e}")
            print(f"✅ Match data saved to {OUTPUT_MATCH_CSV}")
            output_files.append(OUTPUT_MATCH_CSV)
        
        # Scrape stats data
        print(f"\nStarting stats scrape for {STATS_URL}...")
        combined_df = scrape_all_stats_categories(driver, wait, STATS_URL)
        
        if combined_df is not None:
            combined_df.to_csv(OUTPUT_STATS_CSV, index=False)
            print(f"✅ Stats data saved to {OUTPUT_STATS_CSV}")
            print("\n=== Stats Summary ===")
            print(combined_df.head())
            print(f"Total rows: {len(combined_df)}")
            print(f"Categories scraped: {combined_df['Category'].nunique()}")
            output_files.append(OUTPUT_STATS_CSV)
        else:
            print("❌ No stats data collected!")
        
        # Merge all CSV files into one
        if output_files:
            merge_csv_files(output_files, FINAL_CSV, delete_individual=DELETE_INDIVIDUAL_CSVS)
        else:
            print("❌ No files generated to merge!")
            
    except Exception as e:
        print(f"Error in main: {e}")
    
    finally:
        driver.quit()
        print("\nBrowser closed")

if __name__ == "__main__":
    main()