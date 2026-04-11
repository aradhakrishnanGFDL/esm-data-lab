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

    repo = st.text_input("Repository name")

    done = st.checkbox("Created on GitHub")

    if done:
        st.success("Done")

    st.markdown("---")
    st.write("Next: Push code to GitHub")
