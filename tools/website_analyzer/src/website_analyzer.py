from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# class WebsiteAnalyzerTool(BaseTool):
#     name: str = "WebsiteAnalyzer"
#     description: str = "A tool for comprehensive website analysis, including UX assessment, loading speed, mobile responsiveness, content quality, CTA effectiveness, and SEO strategies."

#     def _run(self, url: str) -> str:
#         analyzer = WebsiteAnalyzer(url)
#         results = analyzer.run_analysis()
#         return self.format_results(results)

#     def format_results(self, results):
#         formatted = "Website Analysis Results:\n\n"
#         for key, value in results.items():
#             formatted += f"{key}:\n{value}\n\n"
#         return formatted

class WebsiteAnalyzer:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.driver = None

    def fetch_page(self):
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.content, 'html.parser')

    def setup_selenium(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def analyze_ux(self):
        ux_score = 0
        if self.soup.find('nav'):
            ux_score += 1
        if self.soup.find('footer'):
            ux_score += 1
        if self.soup.find('form'):
            ux_score += 1
        return f"UX Score: {ux_score}/3"

    def analyze_loading_speed(self):
        start_time = time.time()
        requests.get(self.url)
        load_time = time.time() - start_time
        return f"Loading Speed: {load_time:.2f} seconds"

    def analyze_mobile_responsiveness(self):
        self.setup_selenium()
        self.driver.get(self.url)
        self.driver.set_window_size(375, 812)  # iPhone X dimensions
        viewport = self.driver.find_element("css selector", "meta[name='viewport']")
        has_viewport = viewport is not None
        scroll_width = self.driver.execute_script("return document.body.scrollWidth")
        client_width = self.driver.execute_script("return document.documentElement.clientWidth")
        no_horizontal_scroll = scroll_width <= client_width
        self.driver.quit()
        return f"Mobile Responsive: {'Yes' if has_viewport and no_horizontal_scroll else 'No'}"

    def analyze_content_quality(self):
        paragraphs = self.soup.find_all('p')
        word_count = sum(len(p.text.split()) for p in paragraphs)
        headings = self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        return f"Word Count: {word_count}, Number of Headings: {len(headings)}"

    def analyze_cta(self):
        buttons = self.soup.find_all('button')
        links = self.soup.find_all('a', class_=['btn', 'button', 'cta'])
        cta_count = len(buttons) + len(links)
        return f"Number of potential CTAs: {cta_count}"

    def analyze_seo(self):
        title = self.soup.title.string if self.soup.title else "No title"
        meta_description = self.soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_description['content'] if meta_description else "No meta description"
        h1_tags = len(self.soup.find_all('h1'))
        return f"Title: {title}\nMeta Description: {meta_description}\nNumber of H1 tags: {h1_tags}"
    
    
    def analyze_social_media(self):
        social_media = {
            "Facebook": None,
            "Twitter": None,
            "LinkedIn": None,
            "Instagram": None,
            "YouTube": None
        }
        
        # Look for common patterns for social media links
        for a_tag in self.soup.find_all('a', href=True):
            href = a_tag['href'].lower()
            if "facebook.com" in href:
                social_media["Facebook"] = a_tag['href']
            elif "twitter.com" in href or "x.com" in href:
                social_media["Twitter"] = a_tag['href']
            elif "linkedin.com" in href:
                social_media["LinkedIn"] = a_tag['href']
            elif "instagram.com" in href:
                social_media["Instagram"] = a_tag['href']
            elif "youtube.com" in href:
                social_media["YouTube"] = a_tag['href']

        # Format the output to include the links
        formatted_social_media = [f"{platform}: {link}" for platform, link in social_media.items() if link]
        return f"Social Media Presence:\n" + "\n".join(formatted_social_media) if formatted_social_media else "Social Media Presence: None"



    def suggest_improvements(self):
        suggestions = []
        if len(self.soup.find_all('img', alt="")) > 0:
            suggestions.append("Add alt text to all images for better accessibility and SEO.")
        if not self.soup.find('meta', attrs={'name': 'description'}):
            suggestions.append("Add a meta description for better search engine results.")
        if len(self.soup.find_all('a', href="#")) > 0:
            suggestions.append("Replace empty links with meaningful ones or remove them.")
        return "\n".join(suggestions)

    def run_analysis(self):
        self.fetch_page()
        results = {
            "UX Assessment": self.analyze_ux(),
            "Loading Speed": self.analyze_loading_speed(),
            "Mobile Responsiveness": self.analyze_mobile_responsiveness(),
            "Content Quality": self.analyze_content_quality(),
            "CTA Effectiveness": self.analyze_cta(),
            "SEO Strategies": self.analyze_seo(),
            "Social Media Analysis": self.analyze_social_media(),  # Added social media analysis
            "Improvement Suggestions": self.suggest_improvements()
        }
        return results
    
    
website_analyzer = WebsiteAnalyzer(url='https://www.thecreativemomentum.com/')
print(website_analyzer.run_analysis())