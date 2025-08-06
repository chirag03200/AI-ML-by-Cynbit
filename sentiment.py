from textblob import TextBlob

def analyze_sentiment(headlines):
    results = []
    for title in headlines:
        blob = TextBlob(title)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        results.append({"title": title, "sentiment": sentiment})
    return results
