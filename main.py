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
import signal
import sys

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
urls = ["https://www.virgio.com/", "https://www.tatacliq.com/", "https://nykaafashion.com/", "https://www.westside.com/"]

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\nShutting down gracefully... Please wait.")
    save_results()
    sys.exit(0)

def save_results():
    """Save results to both JSON and TXT files"""
    # Save JSON results
    domain_products = defaultdict(list)
    for product_url in crawler.product_urls:
        domain = urlparse(product_url).netloc.replace('www.', '')
        domain_products[domain].append(product_url)
    
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(domain_products, f, indent=2)

    # Save TXT results
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('results.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Crawl Summary - {timestamp}\n")
        f.write(f"{'='*50}\n\n")
        
        f.write("Domains Crawled:\n")
        for url in urls:
            f.write(f"- {url}\n")
        
        f.write(f"\nResults:\n")
        f.write(f"Total products found: {len(crawler.product_urls)}\n")
        f.write(f"Total URLs visited: {len(crawler.visited_urls)}\n\n")
        
        f.write("Product URLs Found:\n")
        for url in crawler.product_urls:
            f.write(f"{url}\n")
        
        f.write(f"\n{'='*50}\n")

    print(f"\nResults saved to results.json and results.txt")

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Create an event to signal the summary thread to stop
stop_summary = threading.Event()

try:
    # Process multiple domains concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(crawler.crawl, urls)
except KeyboardInterrupt:
    print("\nCrawling interrupted by user")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Signal the summary thread to stop
    stop_summary.set()
    
    # Save results even if an error occurred
    save_results()
    
    print("\nCrawling completed!")
    print(f"Total products found: {len(crawler.product_urls)}")
    print(f"Total URLs visited: {len(crawler.visited_urls)}")
    print("Full results are available in results.txt and results.json")