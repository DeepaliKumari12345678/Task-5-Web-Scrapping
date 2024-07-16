import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the e-commerce website
url = 'http://books.toscrape.com/catalogue/category/books_1/index.html'

# Send a GET request to fetch the raw HTML content
response = requests.get(url)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create empty lists to store the product details
    product_names = []
    product_prices = []
    product_ratings = []
    product_availability = []

    # Extract product information
    for product in soup.find_all('article', class_='product_pod'):
        # Extract the product name
        name = product.h3.a['title']
        product_names.append(name)

        # Extract the product price
        price = product.find('p', class_='price_color').text
        product_prices.append(price)

        # Extract the product rating
        rating = product.p['class'][1]
        product_ratings.append(rating)

        # Extract the product availability
        availability = product.find('p', class_='instock availability').text.strip()
        product_availability.append(availability)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame({
        'Product Name': product_names,
        'Price': product_prices,
        'Rating': product_ratings,
        'Availability': product_availability
    })

    # Save the DataFrame to a CSV file
    df.to_csv('books.csv', index=False)

    print('Data has been successfully scraped and saved to books.csv')
else:
    print('Failed to retrieve the webpage')
