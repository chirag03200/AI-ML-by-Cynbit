import requests
from bs4 import BeautifulSoup

def get_hackernews_titles(pages=1, override_page=None):
    titles = []
    base_url = "https://news.ycombinator.com/news?p="

    if override_page is not None:
        pages_to_scrape = [override_page]
    else:
        pages_to_scrape = list(range(1, pages + 1))

    for page in pages_to_scrape:
        res = requests.get(base_url + str(page))
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.select(".titleline > a")
        for link in links:
            titles.append(link.text.strip())

    return titles
