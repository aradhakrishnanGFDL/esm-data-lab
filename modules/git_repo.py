import streamlit as st

  def run():
    # ── Step 1 ───────────────────────────────────────────────────────────────
    st.info("All of the following steps will be done from your Linux terminal. If you're at GFDL, ssh into your workstation and then work on these")
    st.header("1. Clone the repo")
    st.write("Choose your preferred method:")
    st.caption("If you completed Module 2 setting up ssh keys, proceed with SSH option. The HTTPS option requires personal tokens to be entered every time and we will cover that in detail later")
    tab_ssh, tab_https = st.tabs(["SSH (recommended)", "HTTPS"])
    with tab_ssh:
        st.code("git clone git@github.com:your-username/atw_diags.git", language="bash")
        st.write("Replace atw_diags.git with the git repository you created in Module 1")
    with tab_https:
        st.code("git clone https://github.com/your-username/atw_diags.git", language="bash")
        st.write("Refer to https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github#https. This step requires personal access tokens")
    st.write("Then move into the folder:")
    st.code("cd atw_diags", language="bash")

    # ── Step 2 ───────────────────────────────────────────────────────────────
    st.header("2. Add files")
    st.write("Choose whichever applies to you:")
    st.caption("Hint: If you're at GFDL and want to copy over existing diagnostics to continue your work on GitHub, 'Copy existing files, in particular copying over the entire directory is relevant'")

    tab1, tab2 = st.tabs(["Create a new file", "Copy existing files"])

    with tab1:
        st.code("echo 'test' > test.txt", language="bash")

    with tab2:
        st.write("Copy a file from another location into your repo folder:")
        st.code("cp /home/a1r/atw/atw_diags/environment.yaml atw_diags/", language="bash")
        st.write("Or copy an entire directory :")
        st.code("cp -r /home/a1r/atw/atw_diags atw_diags/", language="bash")

    # ── Step 3 ───────────────────────────────────────────────────────────────
    st.header("3. Stage and commit")
    st.code("""
      git add .
      git commit -m "add files"
      """, language="bash")

    # ── Step 4 ───────────────────────────────────────────────────────────────
    st.header("4. Push to GitHub")
    st.code("git push", language="bash")
    st.write("Open your repo on GitHub web interface and go to your repository — you should see your files there.")

    # ── Task ─────────────────────────────────────────────────────────────────

# ── Task ─────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.write("**Your turn:** Follow the steps above using your own repo.")

    completed = st.checkbox("I pushed my first commit")
    if completed:
        repo_url = st.text_input("Paste your GitHub repo URL:")
        git_log = st.text_area("Paste the output of `git log --oneline`:")

        if repo_url and git_log:
            st.success("Done. Your code is now on GitHub. Great job with your first commit")
            st.balloons()

    st.markdown("---")
    #st.write("Next: Branching and pull requests")
