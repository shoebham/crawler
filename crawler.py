from bs4 import BeautifulSoup, SoupStrainer
import requests

from urllib.parse import urljoin

urls=[]
class Crawler:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }

    def crawl(self,url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  
            soup = BeautifulSoup(response.text, "html.parser",parse_only=SoupStrainer('a'))  
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link['href'])
                urls.append(full_url)
                

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")








