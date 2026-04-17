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
    st.write("If you see the file, skip the following step that generates a new key. If not, generate one:")
    st.code('ssh-keygen -t rsa -C "youremail@example.com"', language="bash")
    st.write("Press Enter through all prompts to accept defaults.")
    st.warning("Do not share your private key")
    st.write("Now, add the path to private key to your ssh config")
    st.code("""# Open your SSH config file
    (use your fav editor) ~/.ssh/config
    # Add an entry like this:
    Host github
       HostName github.com
       User git
       IdentityFile ~/.ssh/id_rsa_gh
    """)
    st.write("NEXT - Copy your public copy from the following path")
    st.code("cat ~/.ssh/id_rsa_gh.pub", language="bash")
    st.write("NEXT -  Add it to GitHub: **Settings → SSH and GPG keys → New SSH key** — Type a title, e.g. workstation-gfdl, paste public key in the Key textbox and click 'Add SSH key' ")
    st.write("Test the connection:")
    st.code("ssh -T git@github.com", language="bash")
    st.write("You should see: `Hi your-username! You've successfully authenticated.`")
    st.info("What did we just do? We told our workstation to allow ssh remote access to GitHub using the private key we saved in     our ssh config file; and we told GitHub to associate the matching public key we saved in Github. So, when we try to connect to the server github from our workstation, the key combinations are validated and access is granted. You can now use this to clone github repositories, commit and push changes to it, without having to type passwords. Next module walks through cloning and other git fundamentals")


    st.markdown("### Reflect")

    st.info("This is just for you—your responses are not saved.")

    understood = st.radio(
       "Did you understand the setup?",
       ["Yes", "Somewhat", "Not yet"],
       index=None
    )

    completed = st.checkbox("I completed all steps")
    if not understood or completed:
       st.markdown("Take a moment to ensure you're comfortable before moving on. These steps are required to move to next module")
    if understood or completed:
       st.markdown("Great, lets move on") 
