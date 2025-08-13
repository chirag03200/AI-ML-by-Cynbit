import pandas as pd
import matplotlib.pyplot as plt
import string
import nltk
import streamlit as st
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from io import StringIO

# Download NLTK data
nltk.download('stopwords')
nltk.download('vader_lexicon')

st.set_page_config(page_title="Amazon Review Sentiment Analyzer", layout="wide")
st.title("📦 Amazon Reviews Sentiment Analysis")

st.write("Upload your `.ft.txt` Amazon reviews file to analyze sentiment.")

uploaded_file = st.file_uploader("Choose a .ft.txt file", type=["txt"])

if uploaded_file is not None:
    # ---------------- Load FastText .ft.txt data ----------------
    content = StringIO(uploaded_file.getvalue().decode("utf-8"))
    data = []
    for line in content:
        parts = line.strip().split(" ", 1)
        if len(parts) == 2:
            label = parts[0].replace("__label__", "")
            text = parts[1]
            data.append([label, text])

    df = pd.DataFrame(data, columns=["true_label", "review"])

    # ---------------- Clean text ----------------
    stop_words = set(stopwords.words('english'))

    def clean_text(text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = text.split()
        words = [word for word in words if word not in stop_words]
        return " ".join(words)

    df['cleaned_review'] = df['review'].apply(clean_text)

    # ---------------- Sentiment Analysis ----------------
    sid = SentimentIntensityAnalyzer()

    def get_sentiment_label(text):
        score = sid.polarity_scores(text)['compound']
        if score > 0.05:
            return "Positive"
        elif score < -0.05:
            return "Negative"
        else:
            return "Neutral"

    df['predicted_sentiment'] = df['cleaned_review'].apply(get_sentiment_label)

    # ---------------- Accuracy Calculation ----------------
    label_map = {"1": "Negative", "2": "Positive"}
    df['true_sentiment'] = df['true_label'].map(label_map)
    accuracy = (df['true_sentiment'] == df['predicted_sentiment']).mean() * 100

    st.subheader("📊 Sentiment Distribution")
    sentiment_counts = df['predicted_sentiment'].value_counts()
    fig, ax = plt.subplots()
    sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'], ax=ax)
    ax.set_title('Predicted Sentiment Distribution')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Number of Reviews')
    st.pyplot(fig)

    # ---------------- Show accuracy ----------------
    st.metric(label="Model Accuracy vs True Labels", value=f"{accuracy:.2f}%")

    # ---------------- Show dataframe ----------------
    st.subheader("📄 Analyzed Reviews")
    st.dataframe(df.head(50))

    # ---------------- Download CSV ----------------
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Full Results as CSV",
        data=csv,
        file_name='amazon_reviews_with_sentiment.csv',
        mime='text/csv'
    )
