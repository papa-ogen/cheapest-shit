import requests
from bs4 import BeautifulSoup


# Provider
sort_by = 'PRICE_ASCENDING'
search_query = 'skridskor'
provider_host = 'https://www.xxl.se'
url = f'{provider_host}/search?query={search_query}&sort={sort_by}'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)


# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find elements by HTML data-testid attribute
    products = soup.find_all('div', {'data-testid': 'list-product'})

    print("Found", len(products), "products", products)

    # Print each title
    for product in products:
        print(product.get_text(strip=True))
else:
    print("Failed to retrieve the page. Status code:", response.status_code)