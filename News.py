import streamlit as st
import matplotlib.pyplot as plt
from scraper import scrape_hackernews_headlines
from sentiment import analyze_sentiment

st.set_page_config(page_title="📰 Hacker News Sentiment", layout="centered")
st.title("🧠Trending Topics Sentiment Analyzer (Hacker News)")

pages = st.sidebar.slider("Pages to Scrape", 1, 5, 2)
filter_option = st.sidebar.selectbox("Filter by Sentiment", ["All", "Positive", "Negative", "Neutral"])

with st.spinner("Scraping Hacker News..."):
    raw_headlines = scrape_hackernews_headlines(pages)
    analyzed = analyze_sentiment(raw_headlines)

if filter_option != "All":
    filtered = [x for x in analyzed if x["sentiment"] == filter_option]
else:
    filtered = analyzed

st.subheader(f"Showing {len(filtered)} Headlines ({filter_option})")
for item in filtered:
    st.write(f"**{item['sentiment']}** ➤ {item['title']}")

st.subheader("📊 Sentiment Distribution")
sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
for item in analyzed:
    sentiment_counts[item["sentiment"]] += 1

fig, ax = plt.subplots()
ax.bar(sentiment_counts.keys(), sentiment_counts.values())
ax.set_xlabel("Sentiment")
ax.set_ylabel("Count")
ax.set_title("Hacker News Sentiment")
st.pyplot(fig)
