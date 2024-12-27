import re
from bs4 import BeautifulSoup, SoupStrainer
from patterns import Patterns
import requests

from urllib.parse import urljoin

urls=[]
class Crawler:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    def __init__(self) -> None:
        self.visited_urls = set()
        self.product_urls = set()

        
    def crawl(self,url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  
            soup = BeautifulSoup(response.text, "html.parser",parse_only=SoupStrainer('a'))  
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link['href'])
                if self.is_product_url(full_url):
                    print("Product Found: ",full_url)
                    self.product_urls.add(full_url)

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def is_product_url(self,url):
        patterns = Patterns().get_patterns(url)

        for pattern in patterns["exclude_patterns"]:
            if re.search(pattern,url):
                return False
        
        for pattern in patterns["product_patterns"]:
            if re.search(pattern,url):
                return True
        return False







