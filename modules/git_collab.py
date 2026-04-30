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
<div class="msg">🤝 You're a great collaborator!</div>
"""


def run():
    st.title("Collaborating on GitHub: Merge a Pull Request")
    st.write("""
        You've been working on a branch and your teammate has opened a Pull Request.
        In this module you'll learn how to review and merge it when there are no conflicts.
    """)

    # ── Step 1 ───────────────────────────────────────────────────────────────
    st.header("1. Find the Pull Request")
    st.write("Go to your repository on GitHub and click the **Pull requests** tab. You'll see open PRs listed there.")
    st.write("For e.g. Click on **PR #1 — Merge changes to make notebook catalog**.")

    # ── Step 2 ───────────────────────────────────────────────────────────────
    st.header("2. Review the changes")
    st.write("Click the **Files changed** tab to see exactly what was added or removed.")
    st.info("A line starting with `+` was added. A line starting with `-` was removed.")
    st.write("Also check the **Conversation** tab for any comments from reviewers or automated checks.")

    # ── Step 3 ───────────────────────────────────────────────────────────────
    st.header("3. Confirm there are no conflicts")
    st.write("Scroll to the bottom of the PR. GitHub will show one of two messages:")
    st.success("This branch has no conflicts with the base branch — you're ready to merge.")
    st.error("This branch has conflicts that must be resolved — do not merge yet.")
    st.write("Only proceed when you see the green message. Resolving conflicts is covered in a future module.")  # TODO: link to conflict subtask when ready
    st.write("Green message with no conflicts: This  means the changes in the PR do not overlap with anything in `main` — GitHub can combine them automatically.")
    # ── Step 4 ───────────────────────────────────────────────────────────────
    st.header("4. Merge the Pull Request")
    st.write("Click the green **Merge pull request** button, then **Confirm merge**.")
    st.info("To confirm it worked: go to the **Code** tab of your repo and check that the changes from the PR now appear in the `main` branch.")
    st.info("Learn more: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests")

    # ── Reflect ──────────────────────────────────────────────────────────────
    st.markdown("### Reflect")
    st.info("This is just for you — your responses are not saved.")

    merged_before = st.radio(
        "Have you merged a pull request before?",
        ["Yes", "No — this was my first time"],
        index=None,
    )
    completed = st.checkbox("I reviewed the PR and merged it successfully")

    if merged_before is not None and completed:
        st.components.v1.html(CELEBRATION_HTML, height=60)
    elif merged_before is not None or completed:
        st.markdown("Take your time — go through the steps above and merge the PR before continuing.")
