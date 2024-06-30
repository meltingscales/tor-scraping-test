# tor scraping test

## Why?

I wanted to test how to scrape a website using tor, and none of the existing tools seemed to work for me.

See also https://www.reddit.com/r/TOR/comments/1drs01q/tor_scraping_or_automated_website_crawling/

## Running

```bash
poetry install
poetry run python tor_scraping_test.py
```

## TODO

- [ ] Add an sqlite database to store the results
- [ ] Add a loop to scrape multiple pages
- [ ] Add a config file to store the ports and the proxies
- [ ] Add a way to view progress
- [ ] Add a way to view connections between the websites