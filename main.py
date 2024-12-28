from bs4 import BeautifulSoup, SoupStrainer
import requests
from urllib.parse import urljoin
from crawler import Crawler
import asyncio


crawler = Crawler()
# crawler.crawl("https://www.myntra.com/men-tshirts")
crawler.crawl(start_url="https://www.myntra.com/tshirts/asics/asics-polo-collar-training-t-shirt/27015228/buy")

# print(crawler.product_urls)