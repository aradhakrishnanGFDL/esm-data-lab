import streamlit as st

def run():
    st.title("Module 8: Packaging Python Diagnostics")

    # ── Learning Objectives & Scope ─────────────────────────────────────
    st.info("""
    **What you will learn in this module:**
    * How to turn your diagnostic repository into an installable Python package.
    * How to integrate diagnostics into automated end-to-end computational workflows following climate or weather model runs.
    * How to import your modules (like `atw_diags.utils`) from any directory without managing relative paths or `sys.path`.
    * How to generate executable command-line tools (like `run-atw-diags`) for automated batch jobs.
    * How to inspect and verify package installations using `pip show`.
    
    *Note: This lesson covers **local editable installations** (`pip install -e .`). Publishing to PyPI or installing directly from remote GitHub repositories is highlighted at the end as an advanced option.*
    """)

    # ── 1. Purpose of Packaging & Workflow Automation ───────────────────
    st.header("1. Purpose of Packaging in End-to-End Simulation Workflows")
    
    st.write("""
    In climate and weather modeling, running the numerical model (e.g., SPEAR, AM4, WRF) is only the first step in a computational pipeline. Once the simulation completes on HPC compute nodes, automated post-processing and diagnostic evaluation pipelines must execute headlessly.
    
    Packaging your diagnostic code enables this end-to-end automation:
    
    * **Automated Post-Simulation Pipelines:** Workflow managers (like Slurm, Snakemake, or Cylc) can automatically trigger diagnostic routines as soon as a model run outputs netCDF history files.
    * **Clean Imports Across Scripts:** Submodules (e.g., `from atw_diags.utils import dmget`) can be imported reliably from any directory on the system without hardcoding local file paths.
    * **Standardized CLI Commands:** Exposes terminal commands (like `run-atw-diags`) that batch drivers can invoke directly across compute nodes.
    """)

    # ── 2. How Python Resolves Imports ──────────────────────────────────
    st.header("2. Unpackaged vs. Packaged Imports")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Unpackaged Directory")
        st.write("Requires running scripts directly inside the repository or manually modifying path variables:")
        st.code("""
import sys
sys.path.append("/nbhome/jill.bo/git/atw_diags")

from utils import dmget
""", language="python")
        
    with col2:
        st.subheader("Packaged Directory")
        st.write("Registers the package inside `site-packages` for consistent access:")
        st.code("""
from atw_diags.utils import dmget

# Works from any folder in the active environment
""", language="python")

    # ── 3. Repository Structure ─────────────────────────────────────────
    st.header("3. Repository Setup")
    st.write("A standard package layout uses a `src/` directory for code and `pyproject.toml` for metadata and CLI entry points:")
    
    st.code("""
atw_diags/
├── pyproject.toml
└── src/
    └── atw_diags/
        ├── __init__.py
        ├── utils/
        │   └── dmget.py
        └── workflow/
            └── runner.py
    """, language="text")

    st.write("The `pyproject.toml` file maps terminal commands to internal Python functions:")
    st.code("""
[project.scripts]
run-atw-diags = "atw_diags.workflow.runner:main"
""", language="toml")

    # ── 4. Hands-On Lab ─────────────────────────────────────────────────
    st.header("4. Hands-On: Repository Update, Environment Check & Package Installation")
    
    st.markdown("""
    In previous modules, you cloned the `atw_diags` repository from GitHub (`https://github.com/aradhakrishnanGFDL/atw_diags`). 
    Follow these step-by-step instructions in your GFDL cluster terminal to update your local repository, check your environment, install the package, and test Python imports.
    """)
    st.info("💡 **Starting a brand-new project?** If you are creating a new diagnostic suite from scratch rather than using our cloned repository, jump to **Section 5** to generate a fresh template first.")

    # ── Step 4.1: Repository Setup ──
    st.subheader("Step A: Update Repository & Switch Branch")
    st.write("Navigate into your existing cloned repository directory, pull the latest updates, and switch to the `batch` branch:")
    
    st.code("""
# Navigate into your existing cloned repository directory
cd /nbhome/jill.bo/git/atw_diags

# Fetch latest changes from the remote GitHub repository
git fetch origin

# Update your local tracking branches to match origin
git pull origin

# Switch to the 'batch' branch for this module
git checkout batch
""", language="bash")
    
    st.caption("Note: The `batch` branch contains the packaging configuration (`pyproject.toml`) and driver scripts used in this module. This branch will subsequently be merged into the `main` branch.")

    # ── Step 4.2: Conda Environment Setup ──
    st.subheader("Step B: Conda Environment & pip Verification")
    st.write("""
    Refer to earlier modules where you set up your `spear-analysis` Conda environment. 
    Ensure your active environment has `pip` installed and configured properly so editable mode (`pip install -e .`) functions correctly.
    """)
    
    st.code("""
# Activate your existing Conda environment created in earlier modules
conda activate spear-analysis

# Verify pip is installed in this environment
which pip
# Output should point to: /nbhome/jill.bo/conda/envs/spear-analysis/bin/pip

# Install your local directory in editable mode (-e)
pip install -e .
""", language="bash")

    st.info("""
    **Conda environment.yml Tip for Local Editable Packages:**
    If you manage your environment via an `environment.yml` file, you include local editable installs under the `pip:` section like this:
    ```yaml
    name: spear-analysis
    channels:
      - conda-forge
      - defaults
    dependencies:
      - python=3.14
      - pip
      - pip:
        - -e .
    ```
    """)

    # ── Step 4.3: Inspection ──
    st.subheader("Step C: Inspect Package Registration & CLI Binary")
    st.write("Verify that your package location points to `site-packages` and the `run-atw-diags` CLI binary is placed in your environment PATH:")
    
    st.code("""
# Inspect package metadata, installation path, and dependencies
pip show atw-diags

# Verify that the executable CLI command is mapped inside your environment's bin directory
which run-atw-diags
""", language="bash")

    st.subheader("Sample Output of `pip show atw-diags`")
    st.code("""
Name: atw-diags
Version: 0.1.0
Summary: SPEAR Model Diagnostic Pipeline
Location: /nbhome/jill.bo/conda/envs/spear-analysis/lib/python3.14/site-packages
Requires: numpy, xarray, matplotlib, snakemake, papermill
""", language="text")

    # ── Step 4.4: Python Terminal Testing ──
    st.subheader("Step D: Test Import Access from Python Command Line")
    st.write("To verify that `pip install -e .` worked, change directory outside your repository (e.g., to your home directory) and test importing `atw_diags` directly from the Python terminal:")
    
    st.code("""
# Move to your home directory to prove imports work outside the source folder
cd ~

# Start Python interactive session
python
""", language="bash")

    st.write("Inside the Python prompt (`>>>`), run the following commands:")
    st.code("""
# 1. Import top-level package and inspect its installation path
>>> import atw_diags
>>> print(atw_diags.__file__)
# Output: /nbhome/jill.bo/git/atw_diags/src/atw_diags/__init__.py

# 2. Import submodules directly
>>> import atw_diags.utils as utils
>>> print(dir(utils))

# 3. Import specific functions across submodules
>>> from atw_diags.utils import dmget
>>> print(callable(dmget))
# Output: True

# Exit Python session
>>> exit()
""", language="python")

    # ── 5. Advanced Note on GitHub Repository Templates ─────────────────
    st.header("5. Creating New Diagnostic Packages via GitHub Templates")
    
    st.write("""
    When creating a brand-new diagnostic suite, you don't need to manually write `pyproject.toml` or create the `src/` directory tree from scratch:
    
    1. **Use the GitHub Template:** Visit the `atw_diags` template repository on GitHub and click **"Use this template"** to spawn your own project repository.
    2. **Create New Repository:** Choose 'Create a new repository' to populate the structure automatically.
    3. **Clone to Cluster:** Clone your new repository to your `/nbhome/jill.bo/git/` workspace.
    4. **Register via Pip:** `cd` into your new directory and run `pip install -e .` to link your new package and CLI binary into your active Conda environment.
    """)
    
    # Render the screenshot of the 'Use this template' action
    st.image("assets/new_template.jpeg", caption="Initiating a brand-new project from a GitHub repository template.", use_container_width=True)

    # ── 6. Next Steps / Advanced Distribution ──────────────────────────
    st.header("6. Beyond Local Installation (Advanced)")
    
    st.write("""
    While this module focuses on **local installation**, packaging your code opens up options for broader distribution across teams or HPC systems:
    
    * **Direct Git Installation:** Users can install directly from your GitHub repository URL without cloning it manually first:
      ```bash
      pip install git+[https://github.com/jack.jill/atw_diags.git](https://github.com/jack.jill/atw_diags.git)
      ```
    * **Conda Environment Integration:** Include the git repository URL directly in an `environment.yml` file so team members get the package automatically when building an environment.
    * **PyPI / Private Package Index:** Publish stable versions to PyPI or an internal index for version-controlled releases (`pip install atw-diags`).
    """)

    # ── 7. Review ───────────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Review Questions")

    q1 = st.radio(
        "1. What is the primary benefit of installing your package locally with `pip install -e .` for diagnostic pipelines?",
        [
            "It links local repository code to site-packages, allowing automated workflows to trigger diagnostic tools from any directory.",
            "It uploads the code directly to a public PyPI server.",
            "It converts Python code into binary C executables.",
        ]
    )

    q2 = st.radio(
        "2. Which command lets you verify the exact installation path and registered dependencies of your package?",
        [
            "pip show <package-name>",
            "which python",
            "conda list --env",
        ]
    )

    if st.button("Check Answers"):
        if (
            q1 == "It links local repository code to site-packages, allowing automated workflows to trigger diagnostic tools from any directory."
            and q2 == "pip show <package-name>"
        ):
            st.success("Correct.")
        else:
            st.error("Incorrect. Please review the material above.")
