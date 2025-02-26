from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from fpdf import FPDF

def scrape_ap_temples():
    print("Starting AP Temples data scraping...")
    
    # List of URLs to scrape
    urls = [
        "https://en.wikipedia.org/wiki/List_of_Hindu_temples_in_Andhra_Pradesh",
        "https://en.wikipedia.org/wiki/Category:Hindu_temples_in_Andhra_Pradesh"
    ]

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")

    temples_data = []  # Changed to list of dictionaries

    try:
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)

        # Scrape from first URL (table format)
        print(f"\nScraping from main list...")
        driver.get(urls[0])
        time.sleep(3)

        try:
            # Find the table with temple information
            tables = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.wikitable")))
            
            for table in tables:
                rows = table.find_elements(By.TAG_NAME, "tr")
                
                for row in rows[1:]:  # Skip header row
                    try:
                        cols = row.find_elements(By.TAG_NAME, "td")
                        if len(cols) >= 3:
                            temple_data = {
                                'Temple Name': cols[0].text.strip(),
                                'Deity': cols[1].text.strip(),
                                'Location': cols[2].text.strip(),
                                'Speciality': cols[3].text.strip() if len(cols) > 3 else 'Not specified'
                            }
                            if temple_data['Temple Name']:  # Only add if name exists
                                temples_data.append(temple_data)
                                print(f"Added: {temple_data['Temple Name']}")
                    except Exception as e:
                        print(f"Error processing row: {str(e)}")
                        continue

        except Exception as e:
            print(f"Error with first URL: {str(e)}")

        # Scrape from second URL (category format)
        print(f"\nScraping from category page...")
        driver.get(urls[1])
        time.sleep(3)

        try:
            temple_links = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.mw-category-group ul li a")))
            
            for link in temple_links[:50]:  # Limit to 50 temples from category page
                try:
                    temple_name = link.text.strip()
                    temple_url = link.get_attribute('href')
                    
                    # Visit temple's page
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get(temple_url)
                    time.sleep(2)
                    
                    # Extract information
                    try:
                        deity = driver.find_element(By.XPATH, 
                            "//th[contains(text(), 'Deity')]/following-sibling::td").text.strip()
                    except:
                        deity = "Not specified"
                        
                    try:
                        location = driver.find_element(By.XPATH, 
                            "//th[contains(text(), 'Location')]/following-sibling::td").text.strip()
                    except:
                        location = "Not specified"
                        
                    try:
                        speciality = driver.find_element(By.XPATH, 
                            "//h2[contains(.,'History')]/following-sibling::p[1]").text.strip()
                    except:
                        speciality = "Not specified"
                    
                    temple_data = {
                        'Temple Name': temple_name,
                        'Deity': deity,
                        'Location': location,
                        'Speciality': speciality
                    }
                    temples_data.append(temple_data)
                    print(f"Added: {temple_name}")
                    
                    # Close temple page
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    
                except Exception as e:
                    print(f"Error processing temple link: {str(e)}")
                    if len(driver.window_handles) > 1:
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    continue

        except Exception as e:
            print(f"Error with second URL: {str(e)}")

        # Create DataFrame from collected data
        df = pd.DataFrame(temples_data)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['Temple Name'])

        # Save to CSV
        csv_file = 'ap_temples.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"\nSaved {len(df)} temples to {csv_file}")

        # Create PDF
        pdf = FPDF()
        pdf.add_page('L')
        pdf.set_font("Arial", size=10)
        
        # Add title
        pdf.cell(0, 10, "Famous Hindu Temples in Andhra Pradesh", ln=True, align='C')
        pdf.ln(10)
        
        # Define column widths
        col_widths = [70, 50, 50, 100]
        
        # Add headers
        headers = ['Temple Name', 'Deity', 'Location', 'Speciality']
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 10, header, 1)
        pdf.ln()
        
        # Add data
        for _, row in df.iterrows():
            current_y = pdf.get_y()
            
            # Check if we need a new page
            if current_y > 180:
                pdf.add_page('L')
                # Reprint headers
                for i, header in enumerate(headers):
                    pdf.cell(col_widths[i], 10, header, 1)
                pdf.ln()
                current_y = pdf.get_y()
            
            # Print each cell
            for i, col in enumerate(headers):
                text = str(row[col])[:200]  # Limit text length
                pdf.cell(col_widths[i], 10, text, 1)
            pdf.ln()

        # Save PDF
        pdf_file = 'ap_temples.pdf'
        pdf.output(pdf_file)
        print(f"Converted data to {pdf_file}")

        # Display sample of scraped data
        print("\nSample of temples scraped:")
        print(df[['Temple Name', 'Location', 'Deity']].head().to_string())

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    scrape_ap_temples()