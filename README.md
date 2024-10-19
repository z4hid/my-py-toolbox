# My Python Toolbox

Welcome to **My Python Toolbox** – a collection of handy Python tools designed to simplify common tasks. Whether you're a developer or a data enthusiast, these tools can help you tackle a variety of challenges. This repository will continue to grow as more tools are added, making it your go-to place for Python utilities.

## Tools in This Repository

### 1. Web Scraper

The **Web Scraper** tool uses the Jina API to scrape the content of any given URL. It retrieves web page data and presents it in markdown format, allowing you to easily view or download the scraped content. This tool is perfect for quickly grabbing and processing text from web pages.

#### Features:
- Scrape content from any public URL using the Jina API.
- View the scraped content in markdown format.
- Download the content as a markdown file.
- Easy-to-use Gradio interface.

#### How to Use:

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/my-py-toolbox.git
    cd my-py-toolbox
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Add your Jina API key:
   - Create a `.env` file in the `tools/web_scraper` folder.
   - Add your API key to the `.env` file:
     ```
     JINA_API_KEY=your-api-key
     ```

4. Run the Web Scraper tool:
    ```bash
    cd tools/web_scraper/deployment
    python app.py
    ```

5. You will be able to access the Gradio interface, where you can enter a URL and scrape its content.

#### Running Tests:
To ensure everything is working as expected, run the tests with:
```bash
cd tools/web_scraper/tests
python tests.py
```




