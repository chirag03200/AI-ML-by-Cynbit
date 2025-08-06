import requests
from bs4 import BeautifulSoup

def scrape_hackernews_headlines(pages=1):
    headlines = []
    for page in range(1, pages + 1):
        url = f"https://news.ycombinator.com/news?p={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select(".titleline > a")
        for link in links:
            headlines.append(link.text)
    return list(set(headlines))  # Remove duplicates
