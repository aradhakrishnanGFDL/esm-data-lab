import streamlit as st

CELEBRATION_HTML = """
<style>
  body { margin: 0; background: transparent; }
  @keyframes fadein {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .msg {
    font-family: sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #2e7d32;
    animation: fadein 0.8s ease forwards;
    opacity: 0;
    padding: 12px 0;
  }
</style>
<div class="msg">You're ready to open Pull Requests!</div>
"""

def run():
    st.title("Creating a Pull Request")
    st.write("Before opening a PR, you need a branch to work on. Here's how to create one, make your changes, and open a PR.")

    # ── Step 0: Create a branch ───────────────────────────────────────────────
    st.header("1. Create a branch")
    st.write("It's always a good idea to make changes on a branch, not directly on `main`.")
    st.info("A branch is an isolated version of your code where you can make changes safely. Think of it like keeping a backup of your original code while you develop a new feature — except Git manages that for you automatically through version control.")

    st.write("**Option A: From the terminal, cd into the path where you cloned your git repository**")
    st.code("git checkout -b update-readme", language="bash")
    st.infi("This tells us we are taking the current code version, and branching off to update-readme. This means if you say `git checkout main` at a later point, you can still go back to the main changes. We can talk about merging interactively at some point!")
    st.write("**Option B: From GitHub**")
    st.write("Go to your repo, click the branch dropdown (top left of the file view), type a new branch name, and click **Create branch**.")
    st.info("Best practice: use a short, descriptive branch name like `fix-login-bug` or `update-readme`. When we get to creating GitHub issues, adding the issue number as a prefix is also a great practice.")

    # ── Context ───────────────────────────────────────────────────────────────
    st.divider()
    st.write("**Example:** You created a branch called `update-readme` and edited `README.md`.")
    st.write("Once your changes are committed and pushed (see **Module 3** for `git add`, `git commit`, and `git push`), you're ready to open a PR.")

    # ── Option A ─────────────────────────────────────────────────────────────
    st.header("2. Open a PR from a branch (same repo)")
    st.write("Use this when you're working on a branch inside the same repository as your collaborators.)
    st.write("1. Go to your repo on GitHub.")
    st.write("2. Click the **Compare & pull request** banner that appears after you push, or go to **Pull requests → New pull request**.")
    st.write("3. Make sure the base (destination/to) is `main` and the compare branch (source/from) is `update-readme`.")
    st.write("4. Add a title, short description, and assign a reviewer. Click **Create pull request**.")

    # ── Option B ─────────────────────────────────────────────────────────────
    st.header("3. Open a PR from a fork")
    st.write("Use this when you've forked someone else's repo and want to contribute back.")
    st.write("1. Push your changes to your **fork** on GitHub.")
    st.write("2. Go to the **original** repo (not your fork).")
    st.write("3. Click **Pull requests → New pull request**, then click **compare across forks**.")
    st.write("4. Set the base repo to the original and the head repo to your fork and branch.")
    st.write("5. Add a title, description, and click **Create pull request**.")
    st.info("The maintainer of the original repo will receive your PR and can review or merge it.")
    st.warning("Tip: Say you forked User A's repository — User A's repo is the 'upstream repo' and yours is the fork. Always sync your fork before starting new work, either by running `git pull upstream main` in the terminal, or by clicking **Sync Fork** on your GitHub repo page (just below the branch label). The more out of date your fork, the harder merging becomes — so make it a habit to keep your `main` in sync with upstream.")
    # ── Reflection ───────────────────────────────────────────────────────────
    st.divider()
    st.subheader("Reflection")
    st.write("When would you use a fork instead of a branch in the same repo?")
    with st.expander("See answer"):
        st.write("You fork when you don't have write access to the original repo — for example, contributing to an open-source project. Branches are for when you're already a collaborator on the repo.")

    # ── Celebration ──────────────────────────────────────────────────────────
    st.components.v1.html(CELEBRATION_HTML, height=70)

