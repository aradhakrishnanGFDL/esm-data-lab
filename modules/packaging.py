import streamlit as st

def run_module_8():
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

    # ── 4. Installation and Inspection ─────────────────────────────────
    st.header("4. Hands-On: Local Package Installation")
    
    st.write("Run these commands in your cluster terminal to perform a local editable install:")
    st.code("""
# Navigate to repository root
cd /nbhome/jill.bo/git/atw/atw_diags

# Activate target environment
conda activate spear-analysis-pip

# Install local directory in editable mode
pip install -e .

# Inspect package location and dependencies
pip show atw-diags

# Verify the CLI command binary location
which run-atw-diags
""", language="bash")

    st.subheader("Sample Output of `pip show atw-diags`")
    st.code("""
Name: atw-diags
Version: 0.1.0
Summary: SPEAR Model Diagnostic Pipeline
Location: /nbhome/jill.bo/conda/envs/spear-analysis-pip/lib/python3.14/site-packages
Requires: numpy, xarray, matplotlib, snakemake, papermill
""", language="text")

    # ── 5. Next Steps / Advanced Distribution ──────────────────────────
    st.header("5. Beyond Local Installation (Advanced)")
    
    st.write("""
    While this module focuses on **local installation**, packaging your code opens up options for broader distribution across teams or HPC systems:
    
    * **Direct Git Installation:** Users can install directly from your GitHub repository URL without cloning it manually first:
      ```bash
      pip install git+[https://github.com/jack.jill/atw_diags.git](https://github.com/jack.jill/atw_diags.git)
      ```
    * **Conda Environment Integration:** Include the git repository URL directly in an `environment.yml` file so team members get the package automatically when building an environment.
    * **PyPI / Private Package Index:** Publish stable versions to PyPI or an internal index for version-controlled releases (`pip install atw-diags`).
    """)

    # ── 6. Review ───────────────────────────────────────────────────────
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
