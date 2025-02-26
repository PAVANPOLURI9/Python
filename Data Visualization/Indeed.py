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
    return random.uniform(3.0, 5.0)

def scrape_indeed_jobs(job_title="Data Scientist", location="United States", num_pages=5):
    print("Starting Indeed job scraping...")

    edge_options = Options()
    edge_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    edge_options.add_argument("--window-size=1920,1080")
    edge_options.add_argument("--disable-notifications")
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)

    try:
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=edge_options)
        wait = WebDriverWait(driver, 20)

        # Navigate directly to search results
        search_url = f"https://www.indeed.com/jobs?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}"
        print(f"Navigating to: {search_url}")
        driver.get(search_url)
        time.sleep(get_random_delay())

        jobs_data = []

        for page in range(num_pages):
            print(f"Scraping page {page + 1}...")
            time.sleep(get_random_delay())

            # Scroll slowly down the page
            for i in range(5):
                driver.execute_script(f"window.scrollTo(0, {i * 500});")
                time.sleep(0.5)

            try:
                # Updated selector for job cards
                job_cards = wait.until(EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR, "div.job_seen_beacon")))
                
                print(f"Found {len(job_cards)} jobs on this page")

                for card in job_cards:
                    try:
                        # Scroll element into view
                        driver.execute_script("arguments[0].scrollIntoView(true);", card)
                        time.sleep(random.uniform(0.5, 1.0))

                        # Updated selectors based on new HTML structure
                        try:
                            title = card.find_element(By.CSS_SELECTOR, 
                                "span[id*='jobTitle']").text.strip()
                        except:
                            try:
                                title = card.find_element(By.CSS_SELECTOR, 
                                    "div[class*='css-4qr0g1']").text.strip()
                            except:
                                title = "Not found"

                        try:
                            company = card.find_element(By.CSS_SELECTOR, 
                                "span[data-testid='company-name']").text.strip()
                        except:
                            company = "Not found"

                        try:
                            location = card.find_element(By.CSS_SELECTOR, 
                                "div[data-testid='text-location']").text.strip()
                        except:
                            location = "Not found"

                        try:
                            salary = card.find_element(By.CSS_SELECTOR, 
                                "div[class*='salary-snippet']").text.strip()
                        except:
                            salary = "Not specified"

                        # Only append if we found at least title and company
                        if title != "Not found":
                            jobs_data.append({
                                'Title': title,
                                'Company': company,
                                'Location': location,
                                'Salary': salary
                            })
                            print(f"Scraped: {title[:30]}... at {company}")

                    except Exception as e:
                        print(f"Error scraping individual job: {str(e)}")
                        continue

                # Handle pagination
                if page < num_pages - 1:
                    try:
                        next_link = wait.until(EC.element_to_be_clickable((
                            By.CSS_SELECTOR, "[data-testid='pagination-page-next']")))
                        next_link.click()
                        time.sleep(get_random_delay())
                    except Exception as e:
                        print("Couldn't find next page button, stopping pagination")
                        break

            except Exception as e:
                print(f"Error on page {page + 1}: {str(e)}")
                break

        # Save results to CSV
        if jobs_data:
            df = pd.DataFrame(jobs_data)
            output_file = f'indeed_jobs_{job_title.lower().replace(" ", "_")}.csv'
            df.to_csv(output_file, index=False)
            print(f"\nSuccessfully scraped {len(df)} jobs and saved to {output_file}")
        else:
            print("No jobs were scraped")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    scrape_indeed_jobs(
        job_title="Data Scientist",
        location="New York, NY",  # Using a specific location
        num_pages=5
    )