# data_loader_demo.py
import pandas as pd

# Load data function
def load_data(path):
    df = pd.read_csv(path, sep=';', header=None, names=['text', 'emotion'])
    df['emotion'] = df['emotion'].str.strip().str.lower()
    return df

# Load and preview
if __name__ == "__main__":
    df = load_data("train.txt")
    print(df.head())

# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

def load_data(path):
    df = pd.read_csv(path, sep=';', header=None, names=['text', 'emotion'])
    df['emotion'] = df['emotion'].str.strip().str.lower()
    return df

# Load dataset
df = load_data("train.txt")

# Split data
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['emotion'], test_size=0.2, random_state=42)

# Build pipeline
model = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('clf', MultinomialNB())
])

# Train   
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "emotion_model.pkl")
print("✅ Model saved as emotion_model.pkl")


print(df['emotion'].value_counts())