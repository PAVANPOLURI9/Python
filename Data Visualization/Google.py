from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import csv

# Set up Edge WebDriver using webdriver_manager
options = Options()
options.add_argument("--start-maximized")
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=options)

# Google job search URL
BASE_URL = "https://www.google.com/search?q=Data+Scientist+jobs"

job_list = []

try:
    print("Scraping Google for Data Scientist jobs...")
    driver.get(BASE_URL)
    time.sleep(5)  # Increase wait time to ensure page is fully loaded

    # Find job postings
    try:
        jobs = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.BjJfJf"))
        )
        print(f"Found {len(jobs)} job postings")
    except Exception as e:
        print(f"Error finding job postings: {e}")
        jobs = []  # Ensure jobs is defined as an empty list

    for job in jobs:
        try:
            title = job.find_element(By.CSS_SELECTOR, "div.BjJfJf span").text
            company = job.find_element(By.CSS_SELECTOR, "div.vNEEBe").text
            location = job.find_element(By.CSS_SELECTOR, "div.Qk80Jf").text
            link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            job_list.append([title, company, location, link])
            print(f"Scraped job: {title} at {company}")
        except Exception as e:
            print(f"Error extracting job details: {e}")

    # Save data to CSV file
    with open("google_jobs.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Link"])
        writer.writerows(job_list)
    print("Job postings saved to google_jobs.csv!")

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()  # Close browser