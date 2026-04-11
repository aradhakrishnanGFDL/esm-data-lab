import streamlit as st
from modules import git_intro, github_repo_web

st.sidebar.title("Course")

# All pages
pages = {
    "Home": None,
    "Git Basics": git_intro.run,
    "GitHub Repo (Web)": github_repo_web.run,
}

# Search
search = st.sidebar.text_input("Search")

# Filter pages
if search:
    filtered_pages = {
        name: func
        for name, func in pages.items()
        if search.lower() in name.lower()
    }
else:
    filtered_pages = pages

# Navigation
page = st.sidebar.radio("", list(filtered_pages.keys()))

# Run page
if page == "Home":
    st.title("Welcome ESM Data Lab User")
    st.write("Select a module from the side bar")
else:
    filtered_pages[page]()
