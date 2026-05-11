import streamlit as st
from modules import git_setup, github_repo_web, git_first, git_collab, git_contrib, config_env, run_nb, ide, cimes_internship, data_access

st.sidebar.title("Course Modules")

# Define modules
pages = {
    "home": ("Home", None),
    "github": ("Module 1: GitHub Repo (Web)", github_repo_web.run),
    "git_setup": ("Module 2: Git Basic setup", git_setup.run),
    "git_repo": ("Module 3:  Your first Git workflow", git_first.run), 
    "git_collab": ("Module 4: Collaborating on GitHub", git_collab.run),
    "git_contrib": ("Module 5: Contributing code", git_contrib.run),
    "config_env": ("Module 6: Prepare environment to run notebook", config_env.run),
    "run_nb": ("Module 7: Run an existing notebook", run_nb.run),
    "ide":    ("Module 8: Developing in your IDE", ide.run),
    "data_access": ("Under construction Module 9: Simple data access", data_access.run),
    "cimes_internship": ("BONUS: CIMES Summer Internship 2026", cimes_internship.run),
}

# --- Read URL param ---
query_params = st.query_params
current_module = query_params.get("module", "home")

# --- Sidebar navigation ---
labels = [v[0] for v in pages.values()]
keys = list(pages.keys())

# Find current index
index = keys.index(current_module) if current_module in keys else 0

selected_label = st.sidebar.radio("", labels, index=index, key="nav")

# Map label → key
selected_key = keys[labels.index(selected_label)]

# --- Update URL when user clicks ---
st.query_params["module"] = selected_key

# --- Render page ---
name, func = pages[selected_key]

if selected_key == "home":
    st.title("Welcome ESM Data Lab User")
    st.write("Select a module from the side bar")
elif func is None:
    st.title(name)
    st.write("Coming soon.")
else:
    func()
