import streamlit as st
import pandas as pd

# Store student data across reruns
if 'students' not in st.session_state:
    st.session_state.students = []

# Title
st.title("🎓 Student Directory")

# Sidebar Form to Add a New Student 
st.sidebar.header("➕ Add New Student")
with st.sidebar.form("student_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    course = st.selectbox("Course", ["C++", "Java", "Python", "Web development"])
    score = st.number_input("Score", min_value=0, max_value=100, step=1)
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not name.strip() or not email.strip():
            st.warning("⚠️ Name and Email cannot be empty.")
        else:
            new_student = {
                "Name": name,
                "Email": email,
                "Course": course,
                "Score": score
            }
            st.session_state.students.append(new_student)
            st.success(f"✅ Added {name} to the directory!")

# Display student data
st.subheader("📋 All Students")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)
    st.dataframe(df)

    # Filter section
    st.subheader("🔍 Filter Students")

    # Unique values for dropdowns
    course_options = ["All"] + df["Course"].unique().tolist()
    name_options = ["All"] + df["Name"].unique().tolist()

    selected_course = st.selectbox("Filter by Course", options=course_options)
    selected_name = st.selectbox("Filter by Name", options=name_options)

    # Apply both filters together
    filtered_df = df
    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]
    if selected_name != "All":
        filtered_df = filtered_df[filtered_df["Name"] == selected_name]

    st.write(f"🎯 Showing {len(filtered_df)} student(s) matching filters:")
    st.dataframe(filtered_df)

    # Download button
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_students.csv",
        mime="text/csv"
    )
else:
    st.info("ℹ️ No student data yet. Use the form to add some!")
