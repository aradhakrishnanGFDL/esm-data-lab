import streamlit as st

def run():
    st.title("Create a GitHub Repository")

    st.write("Go to https://github.com and create a new repository.")

    st.write("""
    1. Click "+"
    2. New repository
    3. Name it
    4. Add README
    5. Create
    """)

    st.header("Reflect")

    answer = st.radio(
        "A repository is used to:",
        [
            "Select an answer",
            "Store project files",
            "Install software",
            "Run code"
        ]
    )

    if answer == "Store project files":
        st.success("Correct")
    elif answer == "Select an answer":
        pass
    else:
        st.error("Try again")

    st.header("Task")

    st.write("Create a repository on GitHub (e.g., atw_diags).")
   
    repo_url = st.text_input("Paste your repository URL")

    if repo_url:
       if "github.com" in repo_url and "atw_diags" in repo_url:
           st.success("Looks correct")
       else:
           st.error("Check name or format")

    done = st.checkbox("Created atw_diags")

    if done and repo_url:
       st.success("Done")


    st.header("References")

    st.markdown("""
- https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository
    """)
