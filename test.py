from scraper import scrape_reuters_headlines

headlines = scrape_reuters_headlines(4)
print(f"Found {len(headlines)} headlines:")
for h in headlines:
    print("-", h)
