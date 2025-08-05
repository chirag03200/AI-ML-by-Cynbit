import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import time
from wordcloud import WordCloud

from scraper import get_hackernews_titles
from utils import clean_and_tokenize, get_top_keywords

# 🚀 Page Setup
st.set_page_config(page_title="Trending Topics Extractor", layout="centered")
st.markdown("<h1 style='text-align:center; color:#ff6600;'>🔥 Hacker News Trends</h1>", unsafe_allow_html=True)

# 🛠 Sidebar Settings
with st.sidebar:
    with st.expander("⚙️ Settings", expanded=True):
        page_range = st.slider("Page range to scrape", min_value=1, max_value=5, value=(1, 3))
        live_update = st.toggle("🔄 Auto Refresh Every 30 Seconds")
        min_page, max_page = page_range

# 📡 Scrape Data
with st.spinner(f"Scraping pages {min_page} to {max_page}..."):
    all_headlines = []
    for p in range(min_page, max_page + 1):
        all_headlines.extend(get_hackernews_titles(pages=1, override_page=p))
    words = clean_and_tokenize(all_headlines)
    top_keywords = get_top_keywords(words, top_n=10)

st.success(f"✅ Scraped {len(all_headlines)} headlines from page {min_page} to {max_page}.")

# ☁️ Word Cloud
st.subheader("☁️ Word Cloud of Trending Topics")
wordcloud = WordCloud(width=1000, height=400, background_color='white', colormap='plasma').generate(" ".join(words))
st.image(wordcloud.to_array(), use_container_width=True)

# 📊 Keyword Frequency Chart
st.subheader("📈 Top 10 Keywords Frequency")
labels, counts = zip(*top_keywords)
fig, ax = plt.subplots()
ax.barh(labels, counts, edgecolor="black")
ax.invert_yaxis()
ax.set_xlabel("Frequency")
ax.set_title("Top Keywords")
st.pyplot(fig)

# 📋 Keywords Table
st.subheader("📋 Keywords Table")
df_keywords = pd.DataFrame(top_keywords, columns=["Keyword", "Frequency"])
st.dataframe(df_keywords)

# 💾 CSV Download
st.download_button("📥 Download Keywords CSV", df_keywords.to_csv(index=False), file_name="top_keywords.csv")

# 🔍 Keyword Search
st.subheader("🔍 Search Headlines by Keyword")
keyword = st.text_input("Enter a keyword (e.g. python, games,new)")

if keyword:
    matches = [title for title in all_headlines if keyword.lower() in title.lower()]
    st.success(f"{len(matches)} results found.")
    for title in matches:
        highlighted = title.replace(keyword, f"**:orange[{keyword}]**")
        st.markdown(f"- {highlighted}")

# ℹ️ About
with st.expander("ℹ️ About This App"):
    st.markdown("""
    - Built with Python + Streamlit  
    - Scrapes headlines from [Hacker News](https://news.ycombinator.com)  
    - Extracts trending keywords using basic NLP  
    - Includes live auto-refresh and download options  
    """)

# 🔁 Auto-refresh logic
if live_update:
    st.info("⏳ Live update is ON... refreshing every 30 seconds.")
    time.sleep(30)
    st.rerun()
