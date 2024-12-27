from bs4 import BeautifulSoup, SoupStrainer
import requests
from urllib.parse import urljoin
from crawler import Crawler


crawler = Crawler()
crawler.crawl("https://www.myntra.com/men-tshirts")