import streamlit as st

def run():
    st.title("Git Basics: Your First Commit from Terminal")
    st.write("Version: April 17 update")
    st.write("""
    You've created a repo on GitHub. Now let's get it onto your machine,
    add a file, and push your first commit.
    """)

    st.info("**GFDL users:** SSH into your workstation before continuing.")

    # ── Step 0 ───────────────────────────────────────────────────────────────
    st.header("0. Set up SSH key")
    st.info("An SSH key (e.g., id_rsa) is a secure way to connect your computer to GitHub without using a password. It uses a public/private key pair for authentication. Learn more: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh")
    st.write("Check if you already have one:")
    st.code("ls ~/.ssh/id_rsa_gh", language="bash")
    st.caption("Note: You may provide a different name for the keys")
    st.write("If you see the file, skip to Step 1. If not, generate one:")
    st.code('ssh-keygen -t rsa -C "youremail@example.com"', language="bash")
    st.write("Press Enter through all prompts to accept defaults. Then copy your public key:")
    st.warning("Do not share your private key. Just add it to your ssh config")
    st.code("""# Open your SSH config file
    (use your fav editor) ~/.ssh/config
    # Add an entry like this:
    Host github
       HostName github.com
       User git
       IdentityFile ~/.ssh/id_rsa_gh
    """)
    st.code("cat ~/.ssh/id_rsa_gh.pub", language="bash")
    st.write("Then add it to GitHub: **Settings → SSH and GPG keys → New SSH key** — Type a title, e.g. workstation-gfdl, paste public key in the Key textbox and click 'Add SSH key' ")
    st.write("Test the connection:")
    st.code("ssh -T git@github.com", language="bash")
    st.write("You should see: `Hi your-username! You've successfully authenticated.`")
    st.info("What did we just do? We told our workstation to allow ssh remote access to GitHub using the private key we saved in     our ssh config file; and we told GitHub to associate the matching public key we saved in Github. So, when we try to connect to the server github from our workstation, the key combinations are validated and access is granted. You can now use this to clone github repositories, commit and push changes to it, without having to type passwords")
    # ── Step 1 ───────────────────────────────────────────────────────────────
    st.header("1. Clone the repo")
    st.write("Choose your preferred method:")

    tab_ssh, tab_https = st.tabs(["SSH (recommended)", "HTTPS"])
    with tab_ssh:
        st.code("git clone git@github.com:your-username/atw_diags.git", language="bash")
        st.write("Replace atw_diags.git with the git repository you created in Module 1")
    with tab_https:
        st.write("You'll be prompted for your GitHub username and a **personal access token** (not your password).")
        st.write("Generate one at: **GitHub → Settings → Developer settings → Personal access tokens**")
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

