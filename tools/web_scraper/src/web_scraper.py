import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

JINA_API_KEY = os.getenv('JINA_API_KEY')

def web_scraper(url,api_key):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'X-Locale': 'en-US',
        'X-Return-Format': 'markdown',    
        'X-With-Generated-Alt': 'true',
        'X-With-Links-Summary': 'true'
    }
    scrape_pattern = f'https://r.jina.ai/{url}'
    
    response = requests.get(scrape_pattern, headers=headers)
    return response.text

url = 'https://www.robots.ox.ac.uk/~vgg/data/flowers/102/categories.html'

scrapped = web_scraper(url,JINA_API_KEY)

print(scrapped)
print("===============================================================================")
print(type(scrapped))
print(len(scrapped))
