import streamlit as st

def run():
    st.title("Git Module: Getting Started")

    # Explain
    st.header("Why Git?")
    st.write("""
    Git helps you track changes, collaborate with others, and manage versions of your code.
    """)

    # Show
    st.header("Example")
    st.code("""
git init
git add .
git commit -m "first commit"
""", language="bash")

    st.write("These commands initialize a repository, stage files, and create a commit.")

    # Do (interactive)
    st.header("Try it")

    answer = st.text_input("Which command initializes a repository?")

    if answer:
        if answer.strip() == "git init":
            st.success("Correct")
        else:
            st.error("Try again")

    # Action task
    st.header("Your Task")

    st.write("""
    1. Create a new folder on your machine  
    2. Open a terminal in that folder  
    3. Run the commands shown above  
    4. Create your first commit  
    """)

    completed = st.checkbox("I completed this task")

    if completed:
        st.success("Nice work. Move to the next module when ready.")

    # Next step
    st.markdown("---")
    st.write("Next: Connecting your repository to GitHub and pushing code")
