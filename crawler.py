import re
from bs4 import BeautifulSoup, SoupStrainer
from patterns import Patterns
import requests

from urllib.parse import urljoin
from collections import deque
from queue import Queue
import threading

urls=[]
class Crawler:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    def __init__(self,num_threads=10) -> None:
        self.visited_urls = set()
        self.product_urls = set()
        self.url_queue = Queue()
        self.num_threads = num_threads
        self.url_lock = threading.Lock()  # Add lock for thread-safe operations

    def process_url(self):
        while True:
            try:
                current_url = self.url_queue.get(timeout=5)

                with self.url_lock:
                    if current_url in self.visited_urls:
                        self.url_queue.task_done()
                        continue
                    self.visited_urls.add(current_url)

                print("Crawling", current_url)
                response = requests.get(url=current_url, headers=self.headers)
                response.raise_for_status()

                if self.is_product_url(current_url):
                    print("Product Found: ", current_url)
                    with self.url_lock:
                        self.product_urls.add(current_url)

                soup = BeautifulSoup(response.text, "html.parser",parse_only=SoupStrainer('a'))  
                for link in soup.find_all("a", href=True):
                    full_url = urljoin(current_url, link['href'])
                    self.url_queue.put(full_url)

            except Exception as e:
                print(f"Error: {e}")
            finally:
                self.url_queue.task_done()



    
    def crawl(self, start_url=None):
        self.visited_urls.clear()
        self.product_urls.clear()
        
        if start_url:
            self.url_queue.put(start_url)
            
        threads = []
        for _ in range(self.num_threads):
            t = threading.Thread(target=self.process_url,daemon=True)
            t.start()
            threads.append(t)
        
        self.url_queue.join()
    def is_product_url(self,url):
        patterns = Patterns().get_patterns(url)

        for pattern in patterns["exclude_patterns"]:
            if re.search(pattern,url):
                return False
        
        for pattern in patterns["product_patterns"]:
            if re.search(pattern,url):
                return True
        return False







