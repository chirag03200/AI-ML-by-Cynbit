import streamlit as st
import pandas as pd

# We used st.session_state.students to hold data across reruns
if 'students' not in st.session_state:
    st.session_state.students = []

# Title
st.title("Student Directory")

# Sidebar Form to Add a New Student 
st.sidebar.header("Add New Student")
with st.sidebar.form("student_form"): #st.form means Grouping Inputs Together
    name = st.text_input("Name") # takes text input from the user.
    email = st.text_input("Email")
    course = st.selectbox("Course", ["C++", "Java", "Python", "Web develpoment"]) #Creates a dropdown menu for the user to choose one option.
    score = st.number_input("Score", min_value=0, max_value=100, step=1) # user enter a number using either typing or up/down arrows.
    submitted = st.form_submit_button("Submit") # ek button generate hoga jo value submit krega.

    if submitted:
        new_student = {
            "Name": name,
            "Email": email,
            "Course": course,
            "Score": score
        }
        st.session_state.students.append(new_student) # is se data show hoga hme form of table.but vo data temporarily
        st.success(f"Added {name} to the directory!") # ye hme show hoga side baar ke last me after click on submit button

# Display Table
st.subheader("All Students")
if st.session_state.students:
    df = pd.DataFrame(st.session_state.students)  
    st.dataframe(df) #Showing table
    
    # Filtering by course
    st.subheader("Filter Students")
    selected_course = st.selectbox("Filter by Course", options=["All"] + df["Course"].unique().tolist()) 
    
    if selected_course != "All":
        filtered_df = df[df["Course"] == selected_course]
    else:
        filtered_df = df

    st.write(f"Showing {len(filtered_df)} students enrolled in course: {selected_course}")
    st.dataframe(filtered_df)

    # Filtering by name
    selected_name= st.selectbox("Filter by Name", options=["All"] + df["Name"].unique().tolist())
    if selected_name != "All":
        filtered_df = df[df["Name"] == selected_name]
    else:
        filtered_df = df    

    st.write(f"Showing {len(filtered_df)} student(s) with name: {selected_name}")
    st.dataframe(filtered_df)
    

else:
    st.info("No student data yet. Use the form to add some!")
