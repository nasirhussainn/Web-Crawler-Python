import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class WebCrawler:
    def __init__(self, seed_url, max_pages=1000, output_dir='crawled_pages'):
        self.seed_url = seed_url
        self.max_pages = max_pages
        self.output_dir = output_dir
        self.visited_urls = set()
        self.pages_crawled = 0

        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def crawl(self, url):
        if self.pages_crawled >= self.max_pages:
            return

        if url in self.visited_urls:
            return

        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.visited_urls.add(url)
                self.pages_crawled += 1

                # Parse HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract page title
                page_title = soup.title.text.strip() if soup.title else "Untitled"

                # Extract headings
                headings = [heading.text.strip() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

                # Extract page body
                page_body = soup.get_text().strip()

                # Write to file
                filename = f"{self.pages_crawled}_{page_title}.txt"
                filename = filename.replace('/', '_')  # Remove any slashes in title
                with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
                    f.write(f"URL: {url}\n")
                    f.write(f"Title: {page_title}\n")
                    f.write(f"Headings: {'; '.join(headings)}\n")
                    f.write(f"Body:\n{page_body}\n")

                print(f"Crawled: {url}")

                # Find links on the page and crawl them
                for link in soup.find_all('a', href=True):
                    next_url = urljoin(url, link['href'])
                    self.crawl(next_url)

        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def start_crawl(self):
        self.crawl(self.seed_url)

# Example usage
if __name__ == "__main__":
    seed_url = "https://www.imbd.com"
    crawler = WebCrawler(seed_url)
    crawler.start_crawl()
