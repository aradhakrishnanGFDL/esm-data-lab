import streamlit as st

def run():
    st.title("Module 4: Set Up a Conda Environment")
    st.write("""
    Conda is a package and environment manager. It lets you create isolated environments 
    with specific packages and Python versions — so your project dependencies don't 
    conflict with each other or with other projects on the same machine. It also helps with repeatable analysis environments.
    """)

    st.write("""
    This module walks you through creating and activating a conda environment for your project.
    """)

    st.info("""
    GFDL users: SSH into your workstation first, then run `module load conda` before continuing. 
    This loads a centralized conda installation, so you don't need to install anything.
    
    Other users: Install Miniconda, Anaconda, or Micromamba in your environment. 
    Micromamba is a lightweight alternative to conda — same commands, faster installs.
    """)

    # ── Step 1 ───────────────────────────────────────────────────────────────
    st.header("1. Navigate to your repo")
    st.write("""
    Navigate to your local git repo. For example, if you followed the previous modules 
    and cloned `atw_diags`, cd into it:
    """)
    st.code("cd atw_diags", language="bash")
    st.write("Your repo on GitHub would be at `https://github.com/<yourGitHubHandle>/atw_diags`")

    # ── Step 2 ───────────────────────────────────────────────────────────────
    st.header("2. Create the environment")
    st.write("Choose whichever applies to you:")

    tab1, tab2 = st.tabs(["From environment.yaml", "Create your own"])

    with tab1:
        st.write("""
        The environment name is defined inside `environment.yaml`. 
        Optionally, you can override it with `-n`. The name is what you use 
        to activate the environment later. For example:
        """)
        st.write("For reference, the `atw_diags` repo includes an example `environment.yaml`:")
        st.code("conda env create -n spear-analysis -f environment.yaml", language="bash")
        st.info("Tip: Use a name that reflects the project — you may have many environments on the same machine.")

        st.subheader("Adding a new package")
        st.write("""
        Say you need `cartopy` for map plotting but it wasn't in the original `environment.yaml`. 
        Try installing it from the default conda channel first:
        """)
        st.code("conda install cartopy", language="bash")
        st.write("""
        If conda can't find it, it's likely on conda-forge. A channel is a repository
        where conda looks for packages — the default channel is maintained by Anaconda,
        while conda-forge is a community-driven channel with a much wider package selection:
        """)
        st.code("conda install -c conda-forge cartopy", language="bash")
        st.write("""
        If it's still not found, you can install it with pip. 
        Pip works inside a conda environment — just make sure your environment is active first:
        """)
        st.code("pip install cartopy", language="bash")
        st.write("Once installed, update your `environment.yaml` to capture the change:")
        st.code("conda env export > environment.yaml", language="bash")
        st.info("Tip: Commit the updated `environment.yaml` so your collaborators stay in sync.")

    with tab2:
        st.write("Create a new environment with a name and Python version:")
        st.code("conda create -n my-env python=3.11", language="bash")
        st.write("Then export it as an `environment.yaml` so others can reproduce it:")
        st.code("conda env export > environment.yaml", language="bash")
        st.info("Tip: Commit your `environment.yaml` to your repo so collaborators can recreate your environment exactly.")
        st.info("yaml and yml are both valid extensions, we may use it interchangeably in the tutorial")
    # ── Step 3 ───────────────────────────────────────────────────────────────
    st.header("3. Activate the environment")
    st.code("conda activate your-env-name", language="bash")
    st.write("For example:")
    st.code("conda activate spear-analysis", language="bash")
    st.write("Replace `your-env-name` with the name defined at the top of your `environment.yaml`.")
    st.info("Tip: Check the name with `head -1 environment.yaml` — it's the first line.")

    # ── Step 4 ───────────────────────────────────────────────────────────────
    st.header("4. Verify")
    st.write("Confirm the environment is active and packages are installed:")
    st.code("conda list", language="bash")

    # ── Step 5 ───────────────────────────────────────────────────────────────
    st.header("5. Explore your environment")

    st.subheader("List all conda environments")
    st.code("conda env list", language="bash")

    st.subheader("List packages in active environment")
    st.code("conda list", language="bash")

    st.subheader("Search for a specific package")
    st.code("conda list package-name", language="bash")


    # ── Step 6 ───────────────────────────────────────────────────────────────
    st.header("5. Test your environment")
    st.write("Launch a quick Python session from the terminal to confirm your packages are importable:")
    st.code("python", language="bash")
    st.write("Then try importing xarray:")
    st.code("import xarray as xr\nprint(xr.__version__)", language="python")
    st.write("If no errors appear, your environment is working correctly. Type `exit()` to quit.")
    st.info("Coming up: Testing your environment in Jupyter and VSCode in Module 3.")

    # ── Task ─────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.write("**Your turn:** Create and activate your environment.")

    completed = st.checkbox("I activated my environment")
    if completed:
        env_output = st.text_area("What is the name of your conda environment?")
        if env_output:
            st.success("Nice work. By sharing your environment.yaml you are making your science reproducible.")

    st.markdown("---")
    st.write("Next: Developing in your IDE")
