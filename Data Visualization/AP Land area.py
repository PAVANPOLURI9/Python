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
from fpdf import FPDF

def scrape_ap_land_data():
    print("Starting land use data scraping...")
    
    url = "https://en.wikipedia.org/wiki/Andhra_Pradesh"

    # Set up Chrome options instead of Edge
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        # Use Chrome instead of Edge
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        
        print(f"Navigating to: {url}")
        driver.get(url)
        time.sleep(2)

        # Create a dictionary to store the data
        land_data = {
            'Category': [],
            'Area (km²)': [],
            'Percentage': []
        }

        # Find the Geography section
        geography_section = driver.find_element(By.ID, "Geography")
        
        # Extract land use data from tables or text
        # Note: This is example data - replace with actual scraping logic
        land_data['Category'].extend(['Forest area', 'Agricultural land', 'Water bodies', 'Other'])
        land_data['Area (km²)'].extend(['36,915', '157,000', '5,973', '60,112'])
        land_data['Percentage'].extend(['14.1%', '60%', '2.3%', '23.6%'])

        # Create DataFrame
        df = pd.DataFrame(land_data)
        
        # Save to CSV
        csv_file = 'ap_land_use.csv'
        df.to_csv(csv_file, index=False)
        print(f"\nSaved data to {csv_file}")

        # Convert to PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Add title
        pdf.cell(200, 10, txt="Andhra Pradesh Land Use Data", ln=1, align='C')
        
        # Add column headers
        col_width = pdf.w / 3.0
        pdf.cell(col_width, 10, 'Category', 1)
        pdf.cell(col_width, 10, 'Area (km²)', 1)
        pdf.cell(col_width, 10, 'Percentage', 1)
        pdf.ln()
        
        # Add data
        for index, row in df.iterrows():
            pdf.cell(col_width, 10, str(row['Category']), 1)
            pdf.cell(col_width, 10, str(row['Area (km²)']), 1)
            pdf.cell(col_width, 10, str(row['Percentage']), 1)
            pdf.ln()

        # Save PDF
        pdf_file = 'ap_land_use.pdf'
        pdf.output(pdf_file)
        print(f"Converted data to {pdf_file}")

        # Display the data
        print("\nLand Use Data for Andhra Pradesh:")
        print(df.to_string(index=False))

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    scrape_ap_land_data()