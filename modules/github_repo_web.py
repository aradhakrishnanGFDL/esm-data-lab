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

    st.header("References")

    st.markdown("""
- :contentReference[oaicite:0]{index=0} (main site)  
- https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository  
    """)

    st.header("Check")

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
    elif answer:
        st.error("Try again")



   st.header("Task")

   st.write("Create a repository named `atw_diags` on GitHub.")

   st.write("""
   Follow:
   1. Go to https://github.com
   2. Click "+"
   3. New repository
   4. Name: atw_diags
   5. Add README
   6. Create
   """)

   repo_url = st.text_input("Paste your repository URL")

   if repo_url:
       if "github.com" in repo_url and "atw_diags" in repo_url:
           st.success("Looks correct")
       else:
           st.error("Check name or format")

   done = st.checkbox("Created atw_diags")

   if done and repo_url:
       st.success("Done")
