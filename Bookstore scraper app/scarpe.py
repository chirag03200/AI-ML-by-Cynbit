import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_books(pages=10):
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    all_books = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page}/{pages}...")
        url = base_url.format(page)
        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch page {page}: {e}")
            continue  # skip to next page

        soup = BeautifulSoup(res.text, 'html.parser')
        books = soup.select('article.product_pod')

        for book in books:
            title = book.h3.a['title']
            price_text = book.select_one('p.price_color').text
            price = float(price_text.replace('Â', '').replace('£', '').strip())
            availability = book.select_one('p.instock.availability').text.strip()
            rating_word = book.select_one('p.star-rating')['class'][1]
            rating = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five'].index(rating_word)

            all_books.append({
                'Title': title,
                'Price': price,
                'Availability': availability,
                'Rating': rating
            })

        time.sleep(2)  # be polite to the server

    return pd.DataFrame(all_books)

if __name__ == "__main__":
    print("Starting scraping for all 10 pages...")
    df = scrape_books(pages=10)
    df.to_csv("books.csv", index=False)
    print(f"Done! {len(df)} books saved to 'books.csv'")
