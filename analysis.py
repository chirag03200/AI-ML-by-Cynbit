import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("books.csv")

# Price distribution
plt.figure(figsize=(8, 4))
sns.histplot(df['Price'], bins=20, kde=True)
plt.title("Price Distribution")
plt.xlabel("Price (in £)")
plt.savefig("price_distribution.png")
plt.show()

# Rating count
plt.figure(figsize=(6, 4))
sns.countplot(x='Rating', data=df)
plt.title("Book Ratings Count")
plt.savefig("ratings_count.png")
plt.show()

# Availability
print("\nAvailability count:")
print(df['Availability'].value_counts())