from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# Setup Selenium
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode
driver = webdriver.Chrome(options=chrome_options, service=Service())

# Configuration
BASE_URL = "https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020"
CSV_FILE = "ipl_2020_commentary_all_matches.csv"
MAX_MATCHES = 59  # Up to the second semifinal

# List to store all commentary data
all_commentary = []

try:
    # Step 1: Open the base URL
    print(f"Opening URL: {BASE_URL}")
    driver.get(BASE_URL)
    print("Page loaded. Current URL:", driver.current_url)
    time.sleep(3)

    # Step  정부: Click on "Schedule & Results" tab
    print("Looking for 'Schedule & Results' link...")
    schedule_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@title='IPL 2020 Schedule and Results']"))
    )
    print("Found 'Schedule & Results' link. Clicking...")
    schedule_link.click()
    print("Clicked 'Schedule & Results'. Current URL:", driver.current_url)
    time.sleep(3)

    # Step 3: Get all match links up to match 59
    print("Collecting match links up to the semifinal...")
    match_links = driver.find_elements(By.XPATH, "//a[contains(@class, 'text-hvr-underline')]")
    match_urls = []
    for link in match_links:
        href = link.get_attribute("href")
        if href and "cricket-scores" in href:
            match_urls.append(href)
    match_urls = match_urls[:MAX_MATCHES]  # Limit to 59 matches
    print(f"Found {len(match_urls)} match links to scrape.")

    # Load existing data if it exists to check progress
    if os.path.exists(CSV_FILE):
        existing_df = pd.read_csv(CSV_FILE)
        print(f"Loaded existing data from {CSV_FILE}. Total entries: {len(existing_df)}")
    else:
        existing_df = pd.DataFrame(columns=["Match", "Innings", "Ball", "Commentary"])
        print(f"No existing CSV found. Starting fresh.")

    # Step 4: Loop through each match and scrape commentary
    for match_idx, match_url in enumerate(match_urls, 1):
        try:
            match_name = match_url.split("/")[-1].replace("-vs-", " vs ").replace("-", " ").title()
            print(f"\nProcessing match {match_idx}/{MAX_MATCHES}: {match_url}")

            # Skip if match already fully scraped (check existing data)
            match_existing = existing_df[existing_df["Match"] == match_name]
            if not match_existing.empty:
                innings_summary = match_existing.groupby("Innings").agg({
                    "Ball": [lambda x: min(map(float, x)), lambda x: max(map(float, x))]
                }).reset_index()
                innings_summary.columns = ["Innings", "Min Ball", "Max Ball"]
                fully_scraped = True
                for _, row in innings_summary.iterrows():
                    if row["Min Ball"] > 0.1 or row["Max Ball"] < 15.0:  # Rough check for completeness
                        fully_scraped = False
                        break
                if fully_scraped:
                    print(f"Match {match_name} already fully scraped. Skipping.")
                    continue

            driver.get(match_url)
            time.sleep(5)

            # Step 5: Identify innings tabs
            innings_tabs = []
            try:
                innings_tabs = driver.find_elements(By.XPATH, "//a[contains(@ng-click, 'fetch_commentary') and contains(text(), 'Innings')]")
                if not innings_tabs:
                    print("No innings tabs found. Assuming single innings commentary.")
            except Exception as e:
                print(f"Error locating innings tabs: {e}. Proceeding with default commentary.")

            innings_list = [(None, "Default")] if not innings_tabs else [(tab, tab.text) for tab in innings_tabs]

            # Step 6: Scrape commentary for each innings
            for inning_tab, inning_name in innings_list:
                if inning_tab:
                    try:
                        print(f"Switching to innings: {inning_name}")
                        driver.execute_script("arguments[0].scrollIntoView(true);", inning_tab)
                        time.sleep(1)
                        inning_tab.click()
                        time.sleep(3)
                    except Exception as e:
                        print(f"Error clicking innings tab {inning_name}: {e}. Skipping innings.")
                        continue

                # Step 7: Load all commentary
                print(f"Loading commentary for {inning_name}...")
                max_load_attempts = 50
                load_attempts = 0
                while load_attempts < max_load_attempts:
                    try:
                        load_more_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.ID, "full_commentary_btn"))
                        )
                        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                        time.sleep(1)
                        load_more_button.click()
                        print(f"Clicked 'Load More Commentary' (Attempt {load_attempts + 1}/{max_load_attempts})")
                        load_attempts += 1
                        time.sleep(5)
                    except:
                        print("No 'Load More Commentary' button found or not clickable. Proceeding with scrolling.")
                        break

                # Additional scrolling
                last_height = driver.execute_script("return document.body.scrollHeight")
                max_scroll_attempts = 150
                scroll_attempts = 0
                while scroll_attempts < max_scroll_attempts:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        print("No more new content loaded. Stopping scroll.")
                        break
                    last_height = new_height
                    scroll_attempts += 1
                    print(f"Scroll attempt {scroll_attempts}/{max_scroll_attempts}")
                    ball_elements = driver.find_elements(By.CSS_SELECTOR, "div.cb-mat-mnu-wrp.cb-ovr-num.ng-binding.ng-scope")
                    ball_texts = [elem.text for elem in ball_elements if elem.text.strip()]
                    if ball_texts and any("0.1" in text for text in ball_texts):
                        print("Found 0.1 ball commentary. Stopping scroll.")
                        break

                # Step 8: Scrape commentary
                print(f"Scraping commentary for {inning_name}...")
                commentary_containers = driver.find_elements(By.CSS_SELECTOR, "div.cb-col.cb-col-100.ng-scope")
                if not commentary_containers:
                    print("No commentary containers found. Skipping innings.")
                    continue
                print(f"Found {len(commentary_containers)} commentary containers.")

                # Determine the last ball dynamically
                valid_balls = [float(container.find_element(By.CSS_SELECTOR, "div.cb-mat-mnu-wrp.cb-ovr-num.ng-binding.ng-scope").text.strip())
                               for container in commentary_containers
                               if container.find_elements(By.CSS_SELECTOR, "div.cb-mat-mnu-wrp.cb-ovr-num.ng-binding.ng-scope")]
                last_ball = max(valid_balls) if valid_balls else 20.0  # Default to 20.0 if no valid balls
                print(f"Last ball for {inning_name}: {last_ball}")

                # Determine resume point
                resume_ball = last_ball
                if match_idx == 9 and inning_name == innings_list[0][1]:  # Match 9, first innings
                    resume_ball = 15.3
                    print(f"Resuming Match 9, {inning_name} from ball 15.3")
                elif match_idx == 11 and len(innings_list) > 1 and inning_name == innings_list[1][1]:  # Match 11, second innings
                    resume_ball = 14.6
                    print(f"Resuming Match 11, {inning_name} from ball 14.6")

                # Scrape commentary
                scrape = False
                skipped_count = 0
                for container in commentary_containers:
                    try:
                        ball_elem = container.find_element(By.CSS_SELECTOR, "div.cb-mat-mnu-wrp.cb-ovr-num.ng-binding.ng-scope")
                        ball_text = ball_elem.text.strip()
                        ball_float = float(ball_text)
                    except:
                        skipped_count += 1
                        continue

                    try:
                        comm_elem = container.find_element(By.CSS_SELECTOR, "p.cb-col.cb-col-90")
                        commentary_text = comm_elem.text.strip()
                    except:
                        skipped_count += 1
                        continue

                    if ball_text == "N/A" or commentary_text == "N/A":
                        skipped_count += 1
                        continue

                    if ball_float <= resume_ball:
                        scrape = True
                    if ball_float < 0.1:
                        break

                    if scrape:
                        all_commentary.append({
                            "Match": match_name,
                            "Innings": inning_name,
                            "Ball": ball_text,
                            "Commentary": commentary_text
                        })

                print(f"Skipped {skipped_count} invalid or out-of-range entries for {inning_name}.")

        except Exception as e:
            print(f"Error processing match {match_idx}: {e}. Skipping to next match.")
            continue

    # Step 9: Combine with existing data and save to CSV
    if all_commentary:
        new_df = pd.DataFrame(all_commentary)
        if not existing_df.empty:
            # Remove partial data for specific cases to avoid duplicates
            for match_idx, match_url in enumerate(match_urls[:11], 1):  # Check up to match 11
                match_name = match_url.split("/")[-1].replace("-vs-", " vs ").replace("-", " ").title()
                if match_idx == 9:
                    existing_df = existing_df[~((existing_df["Match"] == match_name) & 
                                               (existing_df["Innings"] == "1st Innings") & 
                                               (existing_df["Ball"].astype(float) >= 15.4))]
                elif match_idx == 11:
                    existing_df = existing_df[~((existing_df["Match"] == match_name) & 
                                               (existing_df["Innings"] == "2nd Innings") & 
                                               (existing_df["Ball"].astype(float) >= 14.6))]
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            combined_df = new_df

        combined_df.to_csv(CSV_FILE, index=False, encoding="utf-8")
        print(f"\nData saved to {CSV_FILE}. Total entries: {len(combined_df)}")

        # Summary
        summary = combined_df.groupby(["Match", "Innings"]).agg({
            "Ball": [lambda x: max(map(float, x)), lambda x: min(map(float, x))]
        }).reset_index()
        summary.columns = ["Match", "Innings", "Max Ball", "Min Ball"]
        print("\nSummary of commentary data:")
        print(summary)
    else:
        print("No new commentary data scraped.")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Current URL at time of error:", driver.current_url)

finally:
    print("Closing browser...")
    time.sleep(5)
    driver.quit()
    print("Browser closed")