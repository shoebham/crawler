import re
from bs4 import BeautifulSoup, SoupStrainer
from patterns import Patterns
import requests

from urllib.parse import urljoin
from collections import deque

urls=[]
class Crawler:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    def __init__(self) -> None:
        self.visited_urls = set()
        self.product_urls = set()
        self.url_queue = deque()
        
    def crawl(self,url):
        self.visited_urls.clear()
        self.product_urls.clear()
        self.url_queue.clear()
        self.url_queue.append(url)
        try:
            while self.url_queue:
                try:
                    current_url = self.url_queue.popleft()
                    print("Crawling",current_url)
                    response = requests.get(url, headers=self.headers)
                    response.raise_for_status()  
                    if current_url in self.visited_urls:
                        continue
                    self.visited_urls.add(current_url)

                    if self.is_product_url(current_url):
                        print("Product Found: ",current_url)
                        self.product_urls.add(current_url)

                    soup = BeautifulSoup(response.text, "html.parser",parse_only=SoupStrainer('a'))  
                    for link in soup.find_all("a", href=True):
                        full_url = urljoin(current_url, link['href'])
                        self.url_queue.append(full_url)

                except Exception as e:
                    print(f"Error: {e}")

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







