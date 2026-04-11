import streamlit as st
from modules import git_intro, github_repo_web

st.sidebar.title("Course")

# Define modules
pages = {
    "home": ("Home", None),
    "git": ("Git Basics", git_intro.run),
    "github": ("GitHub Repo (Web)", github_repo_web.run),
}

# --- Read URL param ---
query_params = st.query_params
current_module = query_params.get("module", "home")

# --- Sidebar navigation ---
labels = [v[0] for v in pages.values()]
keys = list(pages.keys())

# Find current index
index = keys.index(current_module) if current_module in keys else 0

selected_label = st.sidebar.radio("", labels, index=index)

# Map label → key
selected_key = keys[labels.index(selected_label)]

# --- Update URL when user clicks ---
st.query_params["module"] = selected_key

# --- Render page ---
name, func = pages[selected_key]

if selected_key == "home":
    st.title("Welcome ESM Data Lab User")
    st.write("Select a module from the side bar")
else:
    func()
