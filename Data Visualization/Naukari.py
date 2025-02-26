from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random

def get_random_delay():
    return random.uniform(1.5, 3.0)

def scrape_naukri_jobs():
    print("Starting the scraping process...")
    
    # Set up Edge options
    edge_options = Options()
    edge_options.add_argument("--window-size=1920,1080")  # Set window size
    edge_options.add_argument("--disable-notifications")   # Disable notifications
    edge_options.add_argument("--headless")  # Run in headless mode for efficiency
    edge_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    
    try:
        # Initialize Edge WebDriver
        print("Setting up Edge driver...")
        service = Service()
        driver = webdriver.Edge(service=service, options=edge_options)
        driver.implicitly_wait(10)
        
        # Navigate to Naukri.com homepage
        print("Navigating to Naukri.com...")
        driver.get("https://www.naukri.com/")
        time.sleep(5)
        
        wait = WebDriverWait(driver, 20)
        print("Waiting for search interface to load...")
        
        # Find and fill the job title search box
        job_input = wait.until(EC.element_to_be_clickable((By.ID, "qsb-keyword-sugg")))
        job_input.clear()
        time.sleep(1)
        job_input.send_keys("Business Analyst")
        print("Entered job title")
        
        # Find and fill the location search box
        location_input = wait.until(EC.element_to_be_clickable((By.ID, "qsb-location-sugg")))
        location_input.clear()
        time.sleep(1)
        location_input.send_keys("Hyderabad")
        print("Entered location")
        
        # Click the search button
        search_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "qsbSubmit")))
        driver.execute_script("arguments[0].click();", search_button)
        print("Clicked search button")
        
        # Wait for search results to load
        time.sleep(5)
        
        job_titles, companies, locations, descriptions = [], [], [], []
        
        for page in range(5):  # Scraping first 5 pages
            print(f"\nScraping page {page + 1}...")
            time.sleep(5)
            
            try:
                job_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "jobTuple")))
                print(f"Found {len(job_cards)} job cards")
                
                for card in job_cards:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView(true);", card)
                        time.sleep(0.5)
                        
                        title = card.find_element(By.CLASS_NAME, "title").text
                        company = card.find_element(By.CLASS_NAME, "subTitle").text
                        location = card.find_element(By.CLASS_NAME, "location").text
                        description = card.find_element(By.CLASS_NAME, "job-description").text
                        
                        job_titles.append(title)
                        companies.append(company)
                        locations.append(location)
                        descriptions.append(description)
                        
                        print(f"Scraped: {title} at {company}")
                        
                    except Exception as e:
                        print(f"Error scraping job card: {str(e)}")
                        continue
                
                # Pagination: Go to the next page
                try:
                    next_button = driver.find_element(By.CLASS_NAME, "fright" )
                    driver.execute_script("arguments[0].click();", next_button)
                    print("Navigating to next page...")
                    time.sleep(3)
                except:
                    print("No more pages available")
                    break
                
            except Exception as e:
                print(f"Error finding job cards: {str(e)}")
                break
        
        # Save to CSV
        if job_titles:
            print("\nSaving results...")
            jobs_df = pd.DataFrame({
                'Title': job_titles,
                'Company': companies,
                'Location': locations,
                'Description': descriptions
            })
            jobs_df.to_csv('naukri_jobs_hyderabad.csv', index=False)
            print(f"Successfully scraped {len(jobs_df)} jobs and saved to naukri_jobs_hyderabad.csv")
        else:
            print("No jobs were scraped")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        try:
            driver.quit()
            print("Browser closed successfully")
        except:
            print("Error closing browser")

if __name__ == "__main__":
    scrape_naukri_jobs()
