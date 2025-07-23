#  VISITS:-

import streamlit as st

st.title("CHai Maker App")

if st.button("  Make  "):
    st.success("Your  chai is being brewed")

Add_masala =st.checkbox("Add masaale")

if Add_masala:
    st.write("Masala added to your  chai")

tea_type = st.radio("Pick your chai base: ", ["Milk","Water","Almond milk"])    
st.write(f"Selected Base {tea_type}")

flavour = st.selectbox("Choose flavour:", ["Adrak", "Kesar","Tulsi","Ilaaichi"])
st.write(f"Selected flavour {flavour}")

sugar = st.slider("Sugar level (spoon)", 0,5,2)
st.write(f"Selected {sugar} spoon sugar.")

cups = st.number_input("how many cups", min_value=1, max_value=10, step=1)
st.write(f"No of chai :- {cups} cups.")

name = st.text_input("Enter your name:")
if name :
    st.write(f"welcome {name} ! Your chai is on the way")

dob = st.date_input("Select your date of birth")
st.write(f"your date of birth is {dob} ")
