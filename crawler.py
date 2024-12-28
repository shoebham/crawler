import re
from bs4 import BeautifulSoup, SoupStrainer
from patterns import Patterns
import requests

from urllib.parse import urljoin
from collections import deque
from concurrent.futures import ThreadPoolExecutor

urls=[]
MAX_THREADS = 10

class Crawler:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    def __init__(self) -> None:
        self.visited_urls = set()
        self.product_urls = set()
        self.url_queue = deque()
        
    def crawl(self, url):
        self.visited_urls.clear()
        self.product_urls.clear()
        self.url_queue.clear()
        self.url_queue.append(url)
        
        def process_url(current_url):
            try:
                print("Crawling", current_url)
                response = requests.get(current_url, headers=self.headers)
                response.raise_for_status()
                
                if current_url in self.visited_urls:
                    return
                self.visited_urls.add(current_url)

                if self.is_product_url(current_url):
                    print("Product Found: ", current_url)
                    self.product_urls.add(current_url)

                soup = BeautifulSoup(response.text, "html.parser", parse_only=SoupStrainer('a'))
                for link in soup.find_all("a", href=True):
                    full_url = urljoin(current_url, link['href'])
                    if full_url not in self.visited_urls:
                        self.url_queue.append(full_url)
                    
            except Exception as e:
                self.visited_urls.add(current_url)
                print(f"Error processing {current_url}: {e}")

        try:
            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                while self.url_queue:
                    # Process multiple URLs concurrently
                    batch = []
                    for _ in range(MAX_THREADS):
                        if not self.url_queue:
                            break
                        url_to_process = self.url_queue.popleft()
                        if url_to_process not in self.visited_urls:
                            batch.append(url_to_process)
                    
                    if batch:
                        # Execute the batch and wait for completion
                        list(executor.map(process_url, batch))  # Using list() to force waiting
                    
        except Exception as e:
            print(f"Error in crawl: {e}")

    def is_product_url(self,url):
        patterns = Patterns().get_patterns(url)

        for pattern in patterns["exclude_patterns"]:
            if re.search(pattern,url):
                return False
        
        for pattern in patterns["product_patterns"]:
            if re.search(pattern,url):
                return True
        return False







