import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import logging
from urllib.parse import urljoin
import time
import random

logging.basicConfig(level=logging.INFO)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.37",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",
    # Add more user agents as needed
]

def download_pdf(url, user_agent, proxy, folder_path, visited_urls):
    if url in visited_urls:
        logging.info(f"Already visited: {url}")
        return

    headers = {'User-Agent': user_agent}
    proxies = {'http': proxy, 'https': proxy} if proxy else {}
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all links on the page
        links = soup.find_all('a', href=True)
        pdf_links = [link['href'] for link in links if link['href'].endswith('.pdf')]

        if pdf_links:
            logging.info(f"Found {len(pdf_links)} PDF(s) on {url}")
            
            with ThreadPoolExecutor() as executor:
                for pdf_link in pdf_links:
                    pdf_url = pdf_link if pdf_link.startswith('http') else urljoin(url, pdf_link)
                    executor.submit(download_pdf_from_link, pdf_url, user_agent, proxy, folder_path)
        
        visited_urls.add(url)

        # Recursively crawl linked pages
        for link in links:
            next_url = link['href'] if link['href'].startswith('http') else urljoin(url, link['href'])
            download_pdf(next_url, user_agent, proxy, folder_path, visited_urls)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error processing {url}: {e}")

def download_pdf_from_link(pdf_url, user_agent, proxy, folder_path):
    headers = {'User-Agent': user_agent}
    proxies = {'http': proxy, 'https': proxy} if proxy else {}
    
    try:
        response = requests.get(pdf_url, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status()

        # Save the PDF to a local file
        pdf_filename = pdf_url.split("/")[-1]
        pdf_filepath = os.path.join(folder_path, pdf_filename)

        with open(pdf_filepath, 'wb') as pdf_file:
            pdf_file.write(response.content)
        
        logging.info(f"Downloaded: {pdf_filepath}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading PDF from {pdf_url}: {e}")

if __name__ == "__main__":
    # User Input
    target_url = input("Enter the target URL: ")
    use_proxy = input("Do you want to use a proxy? (yes/no): ").lower() == "yes"
    proxy = input("Enter the proxy (e.g., http://your_proxy_ip:your_proxy_port): ") if use_proxy else None
    depth = int(input("Enter the depth for crawling: "))
    num_iterations = int(input("Enter the number of iterations: "))
    folder_path = input("Enter the folder path to save PDFs (default: 'downloads'): ") or 'downloads'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    session = requests.Session()
    visited_urls = set()

    for _ in range(num_iterations):
        user_agent = random.choice(USER_AGENTS)
        logging.info(f"User Agent: {user_agent}")
        download_pdf(target_url, user_agent, proxy, folder_path, visited_urls)
        time.sleep(2)  # Add a delay to avoid rate-limiting and be more considerate
