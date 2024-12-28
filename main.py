from bs4 import BeautifulSoup, SoupStrainer
import requests
from urllib.parse import urljoin, urlparse
from crawler import Crawler
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import threading
import time
import json
from collections import defaultdict

def write_summary(crawler, urls, stop_event):
    """Periodically writes crawling summary to results.txt and results.json"""
    while not stop_event.is_set():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Write txt summary
        with open('results.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Crawl Progress Update - {timestamp}\n")
            f.write(f"{'='*50}\n\n")
            
            f.write("Domains being crawled:\n")
            for url in urls:
                f.write(f"- {url}\n")
            
            f.write(f"\nCurrent Progress:\n")
            f.write(f"Total products found: {len(crawler.product_urls)}\n")
            f.write(f"Total URLs visited: {len(crawler.visited_urls)}\n\n")
            
            f.write("Latest Product URLs Found:\n")
            latest_products = list(crawler.product_urls)[-10:]
            for url in latest_products:
                f.write(f"{url}\n")
            
            f.write(f"\n{'='*50}\n")
        
        # Write JSON summary
        domain_products = defaultdict(list)
        for product_url in crawler.product_urls:
            domain = urlparse(product_url).netloc.replace('www.', '')
            domain_products[domain].append(product_url)
        
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(domain_products, f, indent=2)
        
        # Wait for 2 minutes before next update
        time.sleep(120)

# Initialize crawler
crawler = Crawler()

# List of URLs to crawl
urls = [
    "https://www.myntra.com",
    "https://www.ajio.com",
    "https://www.flipkart.com",
    "https://www.amazon.in",
    "https://www.nykaa.com",
    "https://www.snapdeal.com",
    "https://www.tatacliq.com",
    "https://www.shopclues.com",
    "https://www.firstcry.com",
    "https://www.meesho.com"
]

# Create an event to signal the summary thread to stop
stop_summary = threading.Event()

# Start the summary writer in a separate thread
summary_thread = threading.Thread(target=write_summary, args=(crawler, urls, stop_summary))
summary_thread.start()

try:
    # Process multiple domains concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(crawler.crawl, urls)
finally:
    # Signal the summary thread to stop
    stop_summary.set()
    summary_thread.join()
    
    # Write final JSON summary
    domain_products = defaultdict(list)
    for product_url in crawler.product_urls:
        domain = urlparse(product_url).netloc.replace('www.', '')
        domain_products[domain].append(product_url)
    
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(domain_products, f, indent=2)

# Write final summary
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open('results.txt', 'a', encoding='utf-8') as f:
    f.write(f"\n{'='*50}\n")
    f.write(f"Final Crawl Summary - {timestamp}\n")
    f.write(f"{'='*50}\n\n")
    
    f.write("Domains Crawled:\n")
    for url in urls:
        f.write(f"- {url}\n")
    
    f.write(f"\nFinal Results:\n")
    f.write(f"Total products found: {len(crawler.product_urls)}\n")
    f.write(f"Total URLs visited: {len(crawler.visited_urls)}\n\n")
    
    f.write("All Product URLs Found:\n")
    for url in crawler.product_urls:
        f.write(f"{url}\n")
    
    f.write(f"\n{'='*50}\n")

print("\nCrawling completed!")
print(f"Total products found: {len(crawler.product_urls)}")
print(f"Total URLs visited: {len(crawler.visited_urls)}")
print("Full results are available in results.txt")