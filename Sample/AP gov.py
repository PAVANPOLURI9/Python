from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from fpdf import FPDF

def scrape_ap_mlas():
    print("Starting AP MLAs data scraping...")
    
    # AP Legislative Assembly website
    url = "https://aplegislature.org/web/assembly/members-of-legislative-assembly"

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1920,1080")

    mla_data = []

    try:
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)

        print(f"Navigating to: {url}")
        driver.get(url)
        time.sleep(3)  # Wait for page to load

        # Find and click on current MLAs link if needed
        try:
            # Find the table containing MLA information
            table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row

            for row in rows:
                try:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 4:
                        mla_info = {
                            'Name': cols[1].text.strip(),
                            'Constituency': cols[2].text.strip(),
                            'Party': cols[3].text.strip(),
                            'District': cols[4].text.strip() if len(cols) > 4 else 'Not specified'
                        }
                        mla_data.append(mla_info)
                        print(f"Added: {mla_info['Name']} - {mla_info['Constituency']}")
                except Exception as e:
                    print(f"Error processing row: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error finding table: {str(e)}")

        # Create DataFrame
        df = pd.DataFrame(mla_data)

        # Save to CSV
        csv_file = 'ap_mlas.csv'
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"\nSaved {len(df)} MLAs to {csv_file}")

        # Create PDF
        pdf = FPDF()
        pdf.add_page('L')  # Landscape orientation
        pdf.set_font("Arial", size=10)
        
        # Add title
        pdf.cell(0, 10, "Andhra Pradesh MLAs - Current Assembly", ln=True, align='C')
        pdf.ln(10)
        
        # Define column widths
        col_widths = [60, 60, 40, 50]
        
        # Add headers
        headers = ['Name', 'Constituency', 'Party', 'District']
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
            
            # Print each cell
            for i, col in enumerate(headers):
                text = str(row[col])[:200]  # Limit text length
                pdf.cell(col_widths[i], 10, text, 1)
            pdf.ln()

        # Save PDF
        pdf_file = 'ap_mlas.pdf'
        pdf.output(pdf_file)
        print(f"Converted data to {pdf_file}")

        # Display sample of scraped data
        print("\nSample of MLAs scraped:")
        print(df[['Name', 'Constituency', 'Party']].head().to_string())

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    scrape_ap_mlas()