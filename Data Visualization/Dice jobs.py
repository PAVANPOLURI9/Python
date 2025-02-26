from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
import time
import random

def get_random_delay():
    return random.uniform(2.0, 4.0)

def scrape_dice_jobs(job_title="Business Analyst", location="Boston", num_pages=5):
    print("Starting the scraping process...")

    edge_options = Options()
    # Add these new options to suppress warnings
    edge_options.add_argument('--log-level=3')
    edge_options.add_argument('--silent')
    edge_options.add_argument('--disable-logging')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument("--window-size=1920,1080")
    edge_options.add_argument("--disable-notifications")
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    edge_options.add_experimental_option('useAutomationExtension', False)

    try:
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        wait = WebDriverWait(driver, 20)

        # Navigate to Dice.com
        driver.get("https://www.dice.com")
        time.sleep(get_random_delay())

        # Search inputs
        job_input = wait.until(EC.presence_of_element_located((By.ID, "typeaheadInput")))
        job_input.clear()
        job_input.send_keys(job_title)
        
        location_input = wait.until(EC.presence_of_element_located((By.ID, "google-location-search")))
        location_input.clear()
        location_input.send_keys(location)
        
        search_button = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[data-cy='submit-search-button']")))
        search_button.click()
        
        time.sleep(get_random_delay())

        jobs_data = []

        for page in range(num_pages):
            print(f"Scraping page {page + 1}...")
            time.sleep(get_random_delay())

            job_cards = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "dhi-search-card.ng-star-inserted")))

            for card in job_cards:
                try:
                    title = card.find_element(By.CSS_SELECTOR, "a.card-title-link").text
                    location = card.find_element(By.CSS_SELECTOR, 
                        "span[data-cy='search-result-location']").text
                    
                    # Try to get job type and pay (these might not always be available)
                    try:
                        job_type = card.find_element(By.CSS_SELECTOR, 
                            "span[data-cy='search-result-employment-type']").text
                    except:
                        job_type = "Not specified"
                    
                    try:
                        pay = card.find_element(By.CSS_SELECTOR, 
                            "span[data-cy='search-result-pay-range']").text
                    except:
                        pay = "Not specified"

                    jobs_data.append({
                        'Title': title,
                        'Location': location,
                        'Job Type': job_type,
                        'Pay': pay
                    })

                except Exception as e:
                    continue

            # Handle pagination
            if page < num_pages - 1:
                try:
                    next_page = page + 2
                    pagination = wait.until(EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "li.pagination-page a.page-link")))
                    
                    for link in pagination:
                        if link.text.strip() == str(next_page):
                            driver.execute_script("arguments[0].click();", link)
                            time.sleep(get_random_delay())
                            break
                except:
                    break

        # Save results to CSV
        if jobs_data:
            df = pd.DataFrame(jobs_data)
            output_file = f'dice_jobs_{location.lower().replace(" ", "_")}.csv'
            df.to_csv(output_file, index=False)
            print(f"Successfully scraped {len(df)} jobs and saved to {output_file}")
        else:
            print("No jobs were scraped")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_dice_jobs(
        job_title="Business Analyst",
        location="Boston",
        num_pages=5
    )