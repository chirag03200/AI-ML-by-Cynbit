import streamlit as st

st.title("Hello Streamlit")
st.subheader("Hii streamlit")
st.text("welcome")
st.write("Choose your fav food")

food = st.selectbox("Your fav food: ", ["Daal-Baati", "Chole Bhture", "Paav Bhaji", "Daal-Chaval"])

st.write(f"You choose {food}. Excellent Choice")
st.success("Your food has been brewed")

 