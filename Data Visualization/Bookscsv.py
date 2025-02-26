import os
import requests
import csv
from bs4 import BeautifulSoup

# Define the base URL
base_url = "http://books.toscrape.com/"

# Create a folder to store scraped data
folder_name = "scraped_books_data"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Create a CSV file to store book details
csv_file_path = os.path.join(folder_name, "books_data.csv")

# Open the CSV file for writing
with open(csv_file_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price", "Availability", "Rating", "UPC", "Product Type", "Tax", "Reviews", "Description", "Image Filename", "Book URL"])

    # Send a request to the main page
    response = requests.get(base_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the main page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all books on the main page
        books = soup.find_all('article', class_='product_pod')

        # Loop through each book
        for book in books:
            # Extract book title
            title = book.h3.a['title']
            
            # Extract book price
            price = book.find('p', class_='price_color').text
            
            # Extract availability
            availability = book.find('p', class_='instock availability').text.strip()
            
            # Extract rating
            rating = book.find('p', class_='star-rating')['class'][1]  # Second class contains rating
            
            # Extract book detail page URL
            book_url = base_url + book.h3.a['href'].replace("../", "catalogue/")
            
            # Extract book image URL
            image_url = base_url + book.find('img')['src'].replace('../', '')

            # Send a request to the book detail page
            book_response = requests.get(book_url)
            
            if book_response.status_code == 200:
                book_soup = BeautifulSoup(book_response.text, 'html.parser')

                # Extract description
                description = book_soup.find('meta', attrs={'name': 'description'})
                description_text = description['content'].strip() if description else "No description available"

                # Extract UPC (Unique Product Code)
                upc = book_soup.find('th', text="UPC").find_next_sibling('td').text

                # Extract product type
                product_type = book_soup.find('th', text="Product Type").find_next_sibling('td').text

                # Extract tax amount
                tax = book_soup.find('th', text="Tax").find_next_sibling('td').text

                # Extract number of reviews
                reviews = book_soup.find('th', text="Number of reviews").find_next_sibling('td').text

                # Download and save the book image
                image_filename = title.replace(" ", "_").replace("/", "_") + ".jpg"
                image_path = os.path.join(folder_name, image_filename)
                img_data = requests.get(image_url).content
                with open(image_path, "wb") as img_file:
                    img_file.write(img_data)

                # Write all data to the CSV file
                writer.writerow([title, price, availability, rating, upc, product_type, tax, reviews, description_text, image_filename, book_url])

                print(f"Saved: {title}")
            else:
                print(f"Failed to access book detail page: {book_url}")
    else:
        print("Failed to retrieve the main page.")

print(f"Scraped data stored in '{folder_name}' folder.")