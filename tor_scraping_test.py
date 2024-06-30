from typing import List

import requests
from bs4 import BeautifulSoup

# Tor proxy configuration
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Replace 'your_onion_url' with the actual .onion URL you want to scrape
url = 'http://lockbit7z2jwcskxpbokpemdxmltipntwlkmidcll2qirbu7ykg46eyd.onion'


# Function to get all links from the onion URL
def get_links_from_onion(url: str) -> List[str]:
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


# Fetch and print links
links = get_links_from_onion(url)
for link in links:
    print(link)
