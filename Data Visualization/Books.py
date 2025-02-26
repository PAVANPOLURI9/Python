import requests
from bs4 import BeautifulSoup

# Base URL of the website
base_url = "http://books.toscrape.com/"

# Send a GET request to the main page
response = requests.get(base_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the main page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all book containers
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
        
        # Extract book's detail page URL
        book_url = base_url + "catalogue/" + book.h3.a['href'].replace("../", "")
        
        # Extract book image URL
        image_url = base_url + book.find('img')['src'].replace('../', '')

        # Send request to the book detail page
        book_response = requests.get(book_url)
        
        # Check if book detail page is accessible
        if book_response.status_code == 200:
            book_soup = BeautifulSoup(book_response.text, 'html.parser')
            
            # Extract product description
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

            # Print extracted details
            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Availability: {availability}")
            print(f"Rating: {rating} stars")
            print(f"Image URL: {image_url}")
            print(f"Book URL: {book_url}")
            print(f"UPC: {upc}")
            print(f"Product Type: {product_type}")
            print(f"Tax: {tax}")
            print(f"Number of Reviews: {reviews}")
            print(f"Description: {description_text}")
            print("-" * 100)
        else:
            print(f"Failed to access book detail page: {book_url}")
else:
    print("Failed to retrieve the main page.")
