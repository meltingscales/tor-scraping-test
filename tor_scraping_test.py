import time
from typing import List
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from torscrapingdatabase import TorScrapingDatabase

tsd = TorScrapingDatabase()

# Tor proxy configuration
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Replace 'your_onion_url' with the actual .onion URL you want to scrape
start_url = 'http://lockbit7z2jwcskxpbokpemdxmltipntwlkmidcll2qirbu7ykg46eyd.onion'


def is_url_onion(url: str) -> bool:
    # Extract domain from URL
    parsed = urlparse(url)
    return parsed.netloc.endswith('.onion')


def get_all_links_from_onion(url: str) -> List[str]:
    try:
        response = requests.get(url, proxies=proxies)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [a.get('href') for a in soup.find_all('a', href=True)]
            return links
        else:
            print(f"Error: Received status code {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Error: {e}")
        return []


if __name__ == '__main__':
    # Save the start URL to the database
    tsd.save_url_to_db(start_url, crawled=False)

    while True:
        # Fetch the next URL to crawl
        current_url = tsd.get_next_url()
        print("Going to crawl " + current_url)
        # sleep
        time.sleep(5)
        if not current_url:
            print("No more URLs to crawl. Exiting.")
            break

        # Fetch and print links from the current URL
        links = get_all_links_from_onion(current_url)

        # Mark the current URL as crawled
        tsd.save_url_to_db(current_url, crawled=True)

        print(f"Links from {current_url}:")
        for link in links:
            print(link)

            # check if we've already saved this link
            if not tsd.urls_collection.find_one({'url': link}):
                tsd.save_url_to_db(link, crawled=False)
            else:
                print(f"URL {link} already saved in database")

        # Print the fetched onion links
        onion_links = [link for link in links if is_url_onion(link)]
        print(f"\nOnion links from {current_url}:")
        for onion_link in onion_links:
            print(onion_link)
