import streamlit as st
from Matcher import load_data, vectorize_skills, get_top_matches

st.set_page_config(page_title="Student Skill Matcher", layout="centered")

st.title("🤖 Student Skill Matcher")
st.write("Enter your skills and we'll find you the best collaborators!")

# Load and process
df = load_data()
tfidf, skill_matrix = vectorize_skills(df)

# User input
user_input = st.text_input("🔧 Enter your skills (comma-separated):", "Python, Machine Learning")

if st.button("Find Matches"):
    with st.spinner("Finding best collaborators..."):
        matches = get_top_matches(user_input, df, tfidf, skill_matrix)
        st.subheader("👥 Top Matches:")
        for idx, row in matches.iterrows():
            st.markdown(f"{row['Name']}** - {row['Skills']}")
            st.markdown(f"💯 Match Score: {row['MatchScore (%)']}%")
            st.markdown(f"📂 Project Domain: {row['ProjectDomain']}")
            st.markdown("---")