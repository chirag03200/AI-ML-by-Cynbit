import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("books.csv")

# Apply seaborn style
sns.set(style="whitegrid")

# Price distribution
plt.figure(figsize=(8, 4))
sns.histplot(df['Price'], bins=20, kde=True, color="skyblue")
plt.title("Price Distribution")
plt.xlabel("Price (in ₹)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("price_distribution.png")
plt.show()

# Rating count
plt.figure(figsize=(6, 4))
sns.countplot(x='Rating', data=df, palette="mako")
plt.title("Book Ratings Count")
plt.xlabel("Rating (Stars)")
plt.ylabel("Number of Books")
plt.tight_layout()
plt.savefig("ratings_count.png")
plt.show()

# Availability counts
print("\n📦 Book Availability Count:")
print(df['Availability'].value_counts())