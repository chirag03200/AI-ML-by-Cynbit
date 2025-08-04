import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="📚 BookFindr - Smart Book Explorer", layout="centered")

# Load dataset
df = pd.read_csv("books.csv")

# Sidebar filters
st.sidebar.header("🎯 Find Your Next Favorite Book")
with st.sidebar.form("filters"):
    price_limit = st.slider("💰 Max Price (₹):", 0, int(df['Price'].max()), 30)
    rating = st.selectbox("⭐ Minimum Rating:", [0, 1, 2, 3, 4, 5], index=3)
    submitted = st.form_submit_button("🔍 Search Books")

# Title & description
st.markdown("<h1 style='text-align:center;'>📖 Welcome to BookFindr</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Find books based on price and ratings — now with images! 📸</p>", unsafe_allow_html=True)
st.markdown("---")

# Filter logic
if submitted:
    filtered = df[(df['Price'] <= price_limit) & (df['Rating'] >= rating)]

    st.markdown(f"### 📚 Books under ₹{price_limit} with ⭐ {rating}+ rating")

    if filtered.empty:
        st.warning("🙁 No books match your filters. Try adjusting them.")
    else:
        # Download button
        st.download_button("⬇️ Download Filtered Books", filtered.to_csv(index=False), "filtered_books.csv", "text/csv")

        # Display each book as a card
        for _, row in filtered.iterrows():
            st.markdown(f"""
                <div style="display: flex; gap: 20px; align-items: center; padding: 15px; margin-bottom: 15px;
                            border: 1px solid #ddd; border-radius: 10px; background-color: #f9f9f9;">
                    <img src="{row['Image_URL']}" width="100" style="border-radius: 5px;" />
                    <div>
                        <h4 style="margin-bottom: 5px;">{row['Title']}</h4>
                        <p>💸 <b>Price:</b> ₹{row['Price']} &nbsp;&nbsp;&nbsp; ⭐ <b>Rating:</b> {'⭐' * int(row['Rating'])}</p>
                        <p style="font-size: 14px; color: grey;"><i>{row['Availability']}</i></p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.info("👈 Use the sidebar to filter by price and rating, then click **Search Books**.")
