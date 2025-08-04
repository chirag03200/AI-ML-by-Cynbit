import streamlit as st
import pandas as pd

st.set_page_config(page_title="📚 Bookstore Dashboard", layout="centered")
df = pd.read_csv("books.csv")

st.title("📚 Bookstore Scraper App")

st.dataframe(df)

# Price filter
price_limit = st.slider("Show books below this price (£):", 0, 100, 30)
filtered = df[df['Price'] <= price_limit]
st.write(f"### Books under £{price_limit}")
st.dataframe(filtered)

# Rating filter
rating = st.selectbox("Select minimum rating:", [0, 1, 2, 3, 4, 5])
filtered_rating = df[df['Rating'] >= rating]
st.write(f"### Books with rating ≥ {rating}")
st.dataframe(filtered_rating)