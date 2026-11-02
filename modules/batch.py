import streamlit as st


def run():
    st.title("Module 8: Submitting Batch Jobs with Slurm")

    # ── Header & Repo Reference ──────────────────────────────────────────
    col_title, col_link = st.columns([3, 1])
    with col_title:
        st.caption("Sample Diagnostics (`atw_diags`)")
    with col_link:
        st.markdown(
            "[![GitHub](https://img.shields.io/badge/GitHub-atw__diags-181717?style=flat&logo=github)](https://github.com/NOAA-GFDL/atw_diags)"
        )

    st.write("""
    Interactive exploration in VS Code is ideal for prototyping, but production-scale climate 
    diagnostics (multi-century runs, high-resolution ocean grids) exceed login-node 
    resource limits. This module covers packaging that workflow into a non-interactive, 
    headless batch job on the GFDL analysis cluster via Slurm.
    """)

    # ── Prerequisites & Terminology Recap ────────────────────────────────
    col_pre, col_gloss = st.columns([1, 1])
    with col_pre:
        with st.expander("Prerequisites Recap", expanded=False):
            st.markdown("""
            * **Pip Packaging**: How `run-atw-diags` is registered as a CLI entry point via `pyproject.toml`.
            * **Module 8a (Snakemake & DAGs)**: Dependency tracking, caching targets, and rule definitions.
            * **Module 8b (Papermill)**: Tagging the `parameters` cell to inject runtime filesystem paths headlessly.
            """)
    with col_gloss:
        with st.expander("Glossary Recap", expanded=False):
            st.markdown("""
            * **Slurm (`sbatch`)**: Workload manager allocating compute nodes, cores, memory, and walltime.
            * **Headless Execution**: Running programmatic notebooks start-to-finish without an active UI or web server.
            * **Kernel Registration**: Exposing a specific Conda environment (`spear-analysis`) to Jupyter’s runtime.
            * **DAG (Directed Acyclic Graph)**: Snakemake's dependency tree ensuring prerequisites generate before consumers run.
            """)

    # ── Lifecycle Diagram ────────────────────────────────────────────────
    st.markdown("#### The Batch Lifecycle")
    st.code(
        """
[sbatch driver.sh]
        │
        ▼
┌──────────────────────────────────────────────┐
│ Compute Node Allocation                      │
│   • Directives: 1 node, 4 cores, 32GB RAM    │
│   • Activates environment: spear-analysis    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ CLI Entry Point: run-atw-diags               │
│   • Dynamically resolves repo root & paths   │
│   • Verifies Jupyter kernel registration     │
│   • Hand-off to Snakemake orchestrator       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ Headless Execution Engine (Papermill)        │
│   • Injects absolute paths into parameters   │
│   • Executes notebook cells sequentially     │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ Persisted Artifacts                          │
│   • Slurm logs:  /work/a1r/slurm_<JOB_ID>.out│
│   • Execution:   <out_dir>/*_executed.ipynb  │
│   • Diagnostics: <out_dir>/figures/*.png     │
└──────────────────────────────────────────────┘
    """,
        language="text",
    )

    # ── Script Inspection ────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("1. Inspecting the Batch Script (`driver.sh`)")
    st.write(
        "The submission script (`src/atw_diags/workflow/driver.sh`) wraps resource allocation "
        "and command execution into a reproducible Slurm directive:"
    )

    st.code(
        """#!/bin/bash
#SBATCH --job-name=atw_diags
#SBATCH --output=/work/a1r/slurm_%j.out
#SBATCH --error=/work/a1r/slurm_%j.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --partition=batch

source ~/.bashrc
source $(conda info --base)/etc/profile.d/conda.sh
conda activate spear-analysis-pip

# Invokes the packaged CLI entry point with absolute paths
run-atw-diags \\
    --case /home/a1r/git/atw/atw_diags/configs/atw_atmos_ts_monthly_sfc_ocean_updated_config.json \\
    --settings /home/a1r/git/atw/atw_diags/diagnostics/settings.json \\
    out_dir="/work/a1r/" -w $TMPDIR
""",
        language="bash",
    )

    # ── Job Control & Verification ───────────────────────────────────────
    st.markdown("---")
    st.subheader("2. Job Control & Output Verification")

    st.write("Submit the job and monitor output in real time:")
    st.code(
        """# 1. Submit script to the Slurm queue
sbatch src/atw_diags/workflow/driver.sh

# 2. Check running status on allocated nodes
squeue -u $USER

# 3. Stream live cell execution and Snakemake step progress
tail -f /work/a1r/slurm_<JOB_ID>.out
""",
        language="bash",
    )

    st.write("**Where artifacts live upon completion:**")
    st.markdown("""
    * **`*_executed.ipynb`**: The run artifact containing cell-by-cell execution timings, standard output, and injected variables (`config_path`, `out_dir`).
    * **Figures / NetCDF Datasets**: Saved directly to `/work/a1r/` as dictated by the rule targets.
    * **Slurm Output (`slurm_<JOB_ID>.out`)**: Records environment activations, worker node hostnames, and OS-level exits.
    """)

    # ── Knowledge Check ─────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Knowledge Check")

    q1 = st.radio(
        "1. Why do we run through `run-atw-diags` in `driver.sh` rather than calling `jupyter nbconvert` or interactive VS Code directly?",
        [
            "It guarantees that absolute paths, kernel registrations, and Snakemake DAG dependency checks are handled dynamically inside compute node allocations.",
            "Jupyter notebooks cannot run on compute nodes without an active X11 GUI window.",
            "Slurm requires all analysis code to be converted into C binaries before execution.",
        ],
    )

    q2 = st.radio(
        "2. If a batch run fails mid-computation, where is the most detailed Python-level traceback preserved?",
        [
            "In the default configuration JSON file.",
            "Inside the executed output notebook (`*_executed.ipynb`) at the exact cell that crashed.",
            "In the Git commit history.",
        ],
    )

    if st.button("Check Answers", type="primary"):
        c1 = (
            q1
            == "It guarantees that absolute paths, kernel registrations, and Snakemake DAG dependency checks are handled dynamically inside compute node allocations."
        )
        c2 = (
            q2
            == "Inside the executed output notebook (`*_executed.ipynb`) at the exact cell that crashed."
        )

        if c1 and c2:
            st.success("Correct! Ready to proceed.")
        else:
            st.error("One or more answers need review. Check the trace and retry.")
