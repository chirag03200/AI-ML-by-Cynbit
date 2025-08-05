from collections import Counter
import re

STOPWORDS = set("""
a an and are as at be by for from has he in is it its of on that the to was were will with
this that your you how show using use code open source more
""".split())

def clean_and_tokenize(texts):
    words = []
    for line in texts:
        tokens = re.findall(r'\b[a-z]{3,}\b', line.lower())
        filtered = [word for word in tokens if word not in STOPWORDS]
        words.extend(filtered)
    return words

def get_top_keywords(words, top_n=10):
    return Counter(words).most_common(top_n)
