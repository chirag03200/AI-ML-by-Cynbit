import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import sys
print(sys.executable)

df = pd.read_csv("xAPI-Edu-Data.csv")

# --- Cleaning (same as above) ---
df['gender'] = df['gender'].map({'M': 1, 'F': 0})
df['ParentAnsweringSurvey'] = df['ParentAnsweringSurvey'].map({'Yes': 1, 'No': 0})
df['ParentschoolSatisfaction'] = df['ParentschoolSatisfaction'].map({'Yes': 1, 'No': 0})
df['StudentAbsenceDays'] = df['StudentAbsenceDays'].map({'Under-7': 0, 'Above-7': 1})
df = pd.get_dummies(df, columns=['NationalITy', 'PlaceofBirth', 'StageID', 'GradeID', 'SectionID', 'Topic', 'Semester', 'Relation'])

# Streamlit sections
st.title("📊 School Performance Dashboard")

st.header("Data Summary")
st.write(df.describe())

st.header("🧹 Data Cleaning Steps")
st.markdown("- Dropped nulls\n- Encoded categorical values\n- Normalized numeric features")

st.header("📈 Visualizations")

# Distribution
st.subheader("Class Distribution")
fig1 = sns.countplot(x='Class', data=pd.read_csv("xAPI-Edu-Data.csv"))
st.pyplot(fig1.figure)

#Correlation
st.subheader("Correlation Heatmap")
# Select only numeric columns for correlation
numeric_df = df.select_dtypes(include=['number'])
# Plot the heatmap
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.heatmap(numeric_df.corr(), cmap='coolwarm', ax=ax2, annot=True)
st.pyplot(fig2)


# Streamlit header
st.subheader("Performance by Gender")

# Create a new figure before plotting
fig3, ax = plt.subplots()
sns.countplot(x='Class', hue='gender', data=df, ax=ax)

# Show plot in Streamlit
st.pyplot(fig3)