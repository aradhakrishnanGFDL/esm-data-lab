import streamlit as st
from modules import git_intro

st.sidebar.title("Course Navigation")

page = st.sidebar.selectbox(
    "Choose a module",
    ["Home", "Git Basics"]
)

if page == "Home":
    st.title("Welcome")
    st.write("Select a module from the sidebar")

elif page == "Git Basics":
    git_intro.run()
