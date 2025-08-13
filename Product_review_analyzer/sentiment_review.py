# amazon_reviews_sentiment_ft.py

import pandas as pd
import matplotlib.pyplot as plt
import string
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download NLTK resources
nltk.download('stopwords')
nltk.download('vader_lexicon')

# ---------------- Step 1: Load .ft.txt file ----------------
file_path = "test.ft.txt"

# FastText format: __label__X Review text
data = []
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(" ", 1)  # split into label and text
        if len(parts) == 2:
            label = parts[0].replace("__label__", "")
            text = parts[1]
            data.append([label, text])

df = pd.DataFrame(data, columns=["true_label", "review"])

# ---------------- Step 2: Clean text ----------------
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

# ---------------- Step 3: Sentiment Analysis ----------------
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

# ---------------- Step 4: Visualization ----------------
sentiment_counts = df['predicted_sentiment'].value_counts()

plt.figure(figsize=(6, 4))
sentiment_counts.plot(kind='bar', color=['green', 'red', 'gray'])
plt.title('Sentiment Distribution (Test.ft.txt Data)')
plt.xlabel('Predicted Sentiment')
plt.ylabel('Number of Reviews')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("sentiment_distribution_ft.png")
plt.show()

# ---------------- Step 5: Save results ----------------
df.to_csv('amazon_test_ft_with_sentiment.csv', index=False)
print("✅ Analysis complete! Results saved to 'amazon_test_ft_with_sentiment.csv'")
