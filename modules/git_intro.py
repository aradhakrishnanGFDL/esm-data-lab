import streamlit as st

def run():
    st.title("Git Basics: Your First Commit from Terminal")

    st.write("""
    You've created a repo on GitHub. Now let's get it onto your machine,
    add a file, and push your first commit.
    """)

    # ── Step 1 ───────────────────────────────────────────────────────────────
    st.header("1. Clone the repo")
    st.write("In your terminal, run:")
    st.code("git clone https://github.com/your-username/atw_diags.git", language="bash")
    st.write("Then move into the folder:")
    st.code("cd atw_diags", language="bash")

    # ── Step 2 ───────────────────────────────────────────────────────────────
    st.header("2. Add files")
    st.write("Choose whichever applies to you:")

    tab1, tab2 = st.tabs(["Create a new file", "Copy existing files"])

    with tab1:
        st.code("echo 'hello' > hello.txt", language="bash")

    with tab2:
        st.write("Copy a file from another location into your repo folder:")
        st.code("cp /path/to/your/file.txt atw_diags/", language="bash")
        st.write("Or copy an entire folder:")
        st.code("cp -r /path/to/your/folder atw_diags/", language="bash")

    # ── Step 3 ───────────────────────────────────────────────────────────────
    st.header("3. Stage and commit")
    st.code("""
git add .
git commit -m "add files"
""", language="bash")

    # ── Step 4 ───────────────────────────────────────────────────────────────
    st.header("4. Push to GitHub")
    st.code("git push", language="bash")
    st.write("Open your repo on GitHub — you should see your files there.")

    # ── Task ─────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.write("**Your turn:** Follow the steps above using your own repo.")
    completed = st.checkbox("I pushed my first commit")
    if completed:
        st.success("Done. Your code is now on GitHub.")

    st.markdown("---")
    st.write("Next: Branching and pull requests")
