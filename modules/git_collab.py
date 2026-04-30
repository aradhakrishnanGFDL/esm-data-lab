import streamlit as st


CELEBRATION_HTML = """
<style>
  body { margin: 0; background: transparent; }
  .card {
    margin: 8px 0;
    padding: 28px 20px;
    border-radius: 16px;
    background: linear-gradient(135deg, #0f2027, #1a3a4a, #0f2027);
    text-align: center;
    font-family: sans-serif;
    position: relative;
    overflow: hidden;
  }
  .stars span {
    position: absolute;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #ffd700;
    opacity: 0;
    animation: drift 3s ease-in-out infinite;
  }
  .stars span:nth-child(1) { top:15%; left:10%; animation-delay:0.0s; }
  .stars span:nth-child(2) { top:70%; left:20%; animation-delay:0.3s; }
  .stars span:nth-child(3) { top:30%; left:85%; animation-delay:0.6s; }
  .stars span:nth-child(4) { top:80%; left:75%; animation-delay:0.9s; }
  .stars span:nth-child(5) { top:50%; left:50%; animation-delay:1.2s; }
  .stars span:nth-child(6) { top:10%; left:60%; animation-delay:1.5s; }
  @keyframes drift {
    0%   { opacity:0; transform:translateY(0) scale(1); }
    50%  { opacity:1; transform:translateY(-12px) scale(1.4); }
    100% { opacity:0; transform:translateY(-24px) scale(0.8); }
  }
  .badge {
    font-size: 48px;
    display: inline-block;
    animation: pop 0.6s cubic-bezier(0.175,0.885,0.32,1.275) forwards;
    opacity: 0;
  }
  @keyframes pop {
    0%   { transform:scale(0); opacity:0; }
    100% { transform:scale(1); opacity:1; }
  }
  .title {
    margin: 10px 0 4px;
    font-size: 20px;
    font-weight: 700;
    color: #ffd700;
    animation: fadein 0.5s 0.4s ease forwards;
    opacity: 0;
  }
  .subtitle {
    font-size: 13px;
    color: #a0c8d8;
    animation: fadein 0.5s 0.7s ease forwards;
    opacity: 0;
  }
  @keyframes fadein { to { opacity:1; } }
</style>
<div class="card">
  <div class="stars">
    <span></span><span></span><span></span>
    <span></span><span></span><span></span>
  </div>
  <div class="badge">🤝</div>
  <div class="title">You're a Great Collaborator!</div>
  <div class="subtitle">Subtask 1 complete · Merging a Pull Request</div>
</div>
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
    st.write("Click on the PR you want to review — for example: **PR #42 — Add welcome message to README**.")

    # ── Step 2 ───────────────────────────────────────────────────────────────
    st.header("2. Review the changes")
    st.write("Click the **Files changed** tab to see exactly what was added or removed.")
    st.info("A line starting with `+` was added. A line starting with `-` was removed.")
    st.write("For this PR, you'd see:")
    st.code(
        """# README.md
+ ## Welcome!
+ Thanks for visiting. See CONTRIBUTING.md to get started.""",
        language="diff",
    )
    st.write("Also check the **Conversation** tab for any comments from reviewers or automated checks.")

    # ── Step 3 ───────────────────────────────────────────────────────────────
    st.header("3. Confirm there are no conflicts")
    st.write("Scroll to the bottom of the PR. GitHub will show one of two messages:")
    st.success("This branch has no conflicts with the base branch — you're ready to merge.")
    st.error("This branch has conflicts that must be resolved — do not merge yet.")
    st.write("Only proceed when you see the green message. Resolving conflicts is covered in a future module.")  # TODO: link to conflict subtask when ready

    # ── Step 4 ───────────────────────────────────────────────────────────────
    st.header("4. Merge the Pull Request")
    st.write("Click the green **Merge pull request** button, then **Confirm merge**.")
    st.write("When prompted, click **Delete branch** — the changes are now safely in `main` so the feature branch is no longer needed.")
    st.info("Learn more: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes/merging-a-pull-request")

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
        st.components.v1.html(CELEBRATION_HTML, height=180)
    elif merged_before is not None or completed:
        st.markdown("Take your time — go through the steps above and merge the PR before continuing.")
