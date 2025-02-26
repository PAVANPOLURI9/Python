import os
import pandas as pd
from fpdf import FPDF

# Folder where CSV file is stored
folder_name = "scraped_books_data"
csv_file_path = os.path.join(folder_name, "books_data.csv")

# Read CSV file
df = pd.read_csv(csv_file_path)

# Create a folder to store PDFs
pdf_folder = os.path.join(folder_name, "pdf_reports")
if not os.path.exists(pdf_folder):
    os.makedirs(pdf_folder)

# Function to generate a PDF file for each book
def create_pdf(book_data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='', size=12)

    # Title
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, book_data["Title"], ln=True, align="C")

    pdf.ln(10)  # Add space

    # Book Details
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Price: {book_data['Price']}")
    pdf.multi_cell(0, 10, f"Availability: {book_data['Availability']}")
    pdf.multi_cell(0, 10, f"Rating: {book_data['Rating']} stars")
    pdf.multi_cell(0, 10, f"UPC: {book_data['UPC']}")
    pdf.multi_cell(0, 10, f"Product Type: {book_data['Product Type']}")
    pdf.multi_cell(0, 10, f"Tax: {book_data['Tax']}")
    pdf.multi_cell(0, 10, f"Number of Reviews: {book_data['Reviews']}")
    pdf.multi_cell(0, 10, f"Book URL: {book_data['Book URL']}")

    pdf.ln(5)  # Add space

    # Description
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(0, 10, "Description:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, book_data["Description"])

    # Save PDF with book title as filename
    pdf_filename = f"{book_data['Title'].replace(' ', '_').replace('/', '_')}.pdf"
    pdf_path = os.path.join(pdf_folder, pdf_filename)
    pdf.output(pdf_path)

    print(f"PDF saved: {pdf_filename}")

# Loop through each row in the CSV and create a PDF
for _, row in df.iterrows():
    create_pdf(row)

print(f"All PDFs saved in '{pdf_folder}' folder.")
