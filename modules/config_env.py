import streamlit as st

def run():
    st.title("Module 6: Set Up a Conda Environment")
    st.write("""
    Conda is a package and environment manager. It lets you create isolated environments 
    with specific packages and Python versions — so your project dependencies don't 
    conflict with each other or with other projects on the same machine. It also helps with repeatable analysis environments.
    """)

    st.write("This module walks you through creating and activating a conda environment for your project.")

    st.info("""
    GFDL users: SSH into your workstation first, then run `module load conda` before continuing. 
    This loads a centralized conda installation, so you don't need to install anything.
    
    Other users: Install Miniconda, Anaconda, or Micromamba in your environment. 
    Micromamba is a lightweight alternative to conda — same commands, faster installs.
    We are also exploring the use of Pixi. See the pixi tab to learn more.
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

    tab1, tab2, tab3 = st.tabs(["Conda setup from environment.yaml", "Conda setup from scratch", "pixi - a speedy environment manager"])

    with tab1:
        st.write("For reference, the `atw_diags` repo includes an example `environment.yaml`:")
        st.code("conda env create -n spear-analysis -f environment.yaml", language="bash")
        st.info("Tip: Use a name that reflects the project — you may have many environments on the same machine. Conda environment installation with this reference environment takes at least 10 mins in GFDL environments. If you're curious to be a new tester for pixi setup which is very expedient, checkout the pixi tab.")

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

        # ── Step 3 ──────────────────────────────────────────────────────────
        st.subheader("3. Activate the environment")
        st.code("conda activate your-env-name", language="bash")
        st.write("For example:")
        st.code("conda activate spear-analysis", language="bash")
        st.write("Replace `your-env-name` with the name defined at the top of your `environment.yaml`.")
        st.info("Tip: Check the name with `head -1 environment.yaml` — it's the first line.")

        # ── Step 4 ──────────────────────────────────────────────────────────
        st.subheader("4. Verify")
        st.write("Confirm the environment is active and packages are installed:")
        st.code("conda list", language="bash")

        # ── Step 5 ──────────────────────────────────────────────────────────
        st.subheader("5. Explore your environment")

        st.write("List all conda environments:")
        st.code("conda env list", language="bash")

        st.write("List packages in active environment:")
        st.code("conda list", language="bash")

        st.write("Search for a specific package:")
        st.code("conda list package-name", language="bash")

        # ── Step 6 ──────────────────────────────────────────────────────────
        st.subheader("6. Test your environment")
        st.write("Launch a quick Python session from the terminal to confirm your packages are importable:")
        st.code("python", language="bash")
        st.write("Then try importing xarray:")
        st.code("import xarray as xr\nprint(xr.__version__)", language="python")
        st.write("If no errors appear, your environment is working correctly. Type `exit()` to quit.")
        st.info("Coming up: Testing your environment in Jupyter and VSCode in Module 7.")

    with tab2:
        st.write("Create a new environment with a name and Python version:")
        st.code("conda create -n my-env python=3.11", language="bash")
        st.write("Then export it as an `environment.yaml` so others can reproduce it:")
        st.code("conda env export > environment.yaml", language="bash")
        st.info("Tip: Commit your `environment.yaml` to your repo so collaborators can recreate your environment exactly.")
        st.info("yaml and yml are both valid extensions, we may use it interchangeably in the tutorial.")

        # ── Step 3 ──────────────────────────────────────────────────────────
        st.subheader("3. Activate the environment")
        st.code("conda activate my-env", language="bash")
        st.info("Tip: Check the name with `head -1 environment.yaml` — it's the first line.")

        # ── Step 4 ──────────────────────────────────────────────────────────
        st.subheader("4. Verify")
        st.write("Confirm the environment is active and packages are installed:")
        st.code("conda list", language="bash")

        # ── Step 5 ──────────────────────────────────────────────────────────
        st.subheader("5. Explore your environment")

        st.write("List all conda environments:")
        st.code("conda env list", language="bash")

        st.write("List packages in active environment:")
        st.code("conda list", language="bash")

        st.write("Search for a specific package:")
        st.code("conda list package-name", language="bash")

        # ── Step 6 ──────────────────────────────────────────────────────────
        st.subheader("6. Test your environment")
        st.write("Launch a quick Python session from the terminal to confirm your packages are importable:")
        st.code("python", language="bash")
        st.write("Then try importing xarray:")
        st.code("import xarray as xr\nprint(xr.__version__)", language="python")
        st.write("If no errors appear, your environment is working correctly. Type `exit()` to quit.")
        st.info("Coming up: Testing your environment in Jupyter and VSCode in Module 7.")

    with tab3:
        st.write("Pixi is used to manage reproducible environments for this project.")
        st.subheader("1. Install Pixi (if needed)")
        st.code("curl -fsSL https://pixi.sh/install.sh | sh", language="bash")
        st.subheader("2. Use the existing environment (recommended)")
        st.info(
            "If you were following Modules 1–3, `atw_diags` was used as the example repository: "
            "https://github.com/aradhakrishnanGFDL/atw_diags"
        )
        st.write(
            "If the repository already includes `pixi.toml` and `pixi.lock`, just install the environment:"
        )
        st.code("""
cd atw_diags
pixi install
        """, language="bash")
        st.info("This creates a local `.pixi/` folder containing the environment. In this case, we created it under atw_diags and so atw_diags is the project and the pixi environment corresponds to a specific project, unlike conda.")
        st.subheader("3. Create your own environment (only if needed)")
        st.write("If no `pixi.toml` exists, initialize and add packages:")
        st.code("""
pixi init
pixi add xarray numpy matplotlib cartopy xesmf netcdf4 intake intake-esm jupyter
        """, language="bash")
        st.subheader("4. Test your environment")
        st.write("Activate the environment and verify everything works:")
        st.code("""
pixi shell
python
>>> import xarray as xr
>>> print(xr.__version__)
        """, language="bash")
        st.success("If you see a version number (e.g. 2026.4.0), your environment is working correctly.")

    # ── Task ─────────────────────────────────────────────────────────────────
    st.markdown("---")
    st.write("**Your turn:** Create and activate your environment.")

    completed = st.checkbox("I activated my environment")
    if completed:
        env_output = st.text_area("What is the name of your conda environment? If you're using pixi, what is the name of the project?")
        if env_output:
            st.success("Nice work. By sharing your environment.yaml you are making your science reproducible.")

    st.markdown("---")
    st.write("Next: Module 7 — Running a Jupyter Notebook")