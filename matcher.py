import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
def load_data(path="students_dataset.csv"):
    return pd.read_csv(path)

# Preprocess and vectorize skills
def vectorize_skills(df):
    tfidf = TfidfVectorizer()
    skill_matrix = tfidf.fit_transform(df["Skills"])
    return tfidf, skill_matrix

# Get top N similar students
def get_top_matches(input_skills, df, tfidf, skill_matrix, top_n=3):
    input_vec = tfidf.transform([input_skills])
    similarities = cosine_similarity(input_vec, skill_matrix).flatten()
    top_indices = similarities.argsort()[::-1][:top_n]
    matches = df.iloc[top_indices].copy()
    matches["MatchScore (%)"] = (similarities[top_indices] * 100).round(2)
    return matches