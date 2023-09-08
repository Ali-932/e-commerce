from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import os
import base64

book_titles = ['chainsaw man volume 1', 'chainsaw man volume 2', 'chainsaw man volume 3']

# Set up Selenium WebDriver
driver = webdriver.Chrome()
driver.get("https://www.google.com")

for title in book_titles:
    search_query = title.replace(' ', '+')
    search_url = f'https://www.google.com/search?q={search_query}&tbm=isch'
    driver.get(search_url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all the img tags within the page source
    search_result = soup.find('div', {'class': 'rg_meta'})
    print(search_result)
    # Process the images as needed
    # for i, image in enumerate(images):
    #     # Example: Print the image source URL
    #     src = image['src']
    #
    #     # Download the image
    #     response = requests.get(src)
    #
    #     # Save the image to a file
    #     # Remove any trailing characters that are not part of the base64 encoding
    #     content = response.content.rstrip(b'\n-= ')
    #
    #     # Decode the base64-encoded image data
    #     try:
    #         image_data = base64.b64decode(content)
    #     except base64.binascii.Error:
    #         print(f"Invalid base64-encoded image data for image {i}. Skipping...")
    #         continue
    #
    #     with open(os.path.join('', f'image_{i}.jpg'), 'wb') as f:
    #         f.write(response.content)
    #
    #     print(f"Image {i} downloaded.")

# Close the WebDriver
driver.quit()
