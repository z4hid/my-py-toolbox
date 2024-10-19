import gradio as gr
import requests
import os
import tempfile
from dotenv import load_dotenv
from typing import Tuple

# Load environment variables from .env file
load_dotenv()

JINA_API_KEY = os.getenv('JINA_API_KEY')

def web_scraper(url: str) -> str:
    """
    Scrape the content of a given URL using the Jina API.

    Args:
        url (str): The URL to scrape.

    Returns:
        str: The scraped content in markdown format.
    """
    headers = {
        'Authorization': f'Bearer {JINA_API_KEY}',
        'X-Locale': 'en-US',
        'X-Return-Format': 'text',    
        'X-With-Generated-Alt': 'true',
        'X-With-Links-Summary': 'true'
    }
    scrape_pattern = f'https://r.jina.ai/{url}'
    
    response = requests.get(scrape_pattern, headers=headers)
    return response.text

def scrape_and_display(url: str) -> Tuple[str, tempfile._TemporaryFileWrapper]:
    """
    Scrape the content of a given URL and prepare it for display and download.

    Args:
        url (str): The URL to scrape.

    Returns:
        Tuple[str, tempfile._TemporaryFileWrapper]: A tuple containing the scraped content and a temporary file for download.
    """
    scraped_content = web_scraper(url)
    
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(mode="w+", suffix=".md", delete=False)
    temp_file.write(scraped_content)
    temp_file.flush()
    
    return scraped_content, temp_file.name

def create_gradio_interface() -> gr.Interface:
    """
    Create and configure the Gradio interface for the web scraper.

    Returns:
        gr.Interface: The configured Gradio interface.
    """
    return gr.Interface(
        fn=scrape_and_display,
        inputs=gr.Textbox(label="Enter URL to scrape"),
        outputs=[
            gr.Markdown(label="Scraped Content"),
            gr.File(label="Download Markdown")
        ],
        title="Web Scraper",
        description="Enter a URL to scrape and view the content in markdown format. You can also download the markdown file.",
        examples=[["https://www.robots.ox.ac.uk/~vgg/data/flowers/102/categories.html"]],
        allow_flagging="never"
    )

if __name__ == "__main__":
    iface = create_gradio_interface()
    iface.launch()