import streamlit as st


def run():
    st.title("Module 10: Submitting Batch Jobs with Slurm")

    # ── Header & Repo Reference ──────────────────────────────────────────
    col_title, col_link = st.columns([3, 1])
    with col_title:
        st.caption("Sample Diagnostics Pipeline (`atw_diags`)")
    with col_link:
        st.markdown(
            "[![GitHub](https://img.shields.io/badge/GitHub-atw__diags-181717?style=flat&logo=github)](https://github.com/NOAA-GFDL/atw_diags)"
        )

    st.write("""
    Interactive exploration in VS Code is ideal for prototyping, but production-scale 
    diagnostics exceed login-node resource limits. This module covers packaging 
    that workflow into a non-interactive, headless batch job on the GFDL analysis cluster via Slurm.
    """)

    # ── Prerequisites & Terminology Recap ────────────────────────────────
    col_pre, col_gloss = st.columns([1, 1])
    with col_pre:
        with st.expander("Prerequisites Recap", expanded=False):
            st.markdown("""
            * **Module 8 (Packaging with Pip)**: In Module 8, you installed the package in editable mode:
              ```bash
              pip install -e .
              ```
              This links the codebase directly into your environment and exposes the **`run-atw-diags`** CLI entry point globally across your terminal.
            * **Module 9 (Snakemake and Friends)**: DAG resolution, caching output targets, and using Papermill to inject paths into the `parameters` cell.
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
[sbatch driver.sh]  OR  [sbatch vanilla_driver.sh]
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
│ Orchestration Choice                         │
│   • Dev: Direct Snakemake call (Vanilla)     │
│   • Prod: CLI entry point (run-atw-diags)    │
│           (Available via 'pip install -e .') │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│ Headless Execution Engine (Papermill - Mod 9)│
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

    # ── Two Approaches: Vanilla vs Packaged ──────────────────────────────
    st.markdown("---")
    st.subheader("1. Choosing Your Driver: Dev vs. Production")
    st.write("""
    Depending on whether you are actively developing code or submitting production runs, 
    two driver scripts are provided in `src/atw_diags/workflow/`:
    """)

    tab_vanilla, tab_packaged = st.tabs(
        ["🛠️ Development Mode (`vanilla_driver.sh`)", "🚀 Production Mode (`driver.sh`)"]
    )

    with tab_vanilla:
        st.markdown("##### Direct Developer Execution (`vanilla_driver.sh`)")
        st.write("""
        Ideal for rapid local development when you want to bypass package entry points 
        and execute `snakemake` directly against the raw repo files.
        """)

        st.code(
            """#!/bin/bash
#SBATCH --job-name=atw_dev
#SBATCH --output=/work/a1r/slurm_%j.out
#SBATCH --error=/work/a1r/slurm_%j.err
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --partition=batch

set -e

# 1. Manually cd into repo root
cd /home/a1r/git/atw/atw_diags

# 2. Activate Conda environment directly
source $(conda info --base)/etc/profile.d/conda.sh
conda activate spear-analysis

# 3. Direct Snakemake call pointing to the local Snakefile
snakemake -s src/atw_diags/workflow/Snakefile \\
    --cores 4 \\
    --config \\
        case_path="/home/a1r/git/atw/atw_diags/configs/atw_atmos_ts_monthly_sfc_ocean_updated_config.json" \\
        settings_path="/home/a1r/git/atw/atw_diags/diagnostics/settings.json" \\
        out_dir="/work/a1r/" \\
    -F
""",
            language="bash",
        )

        st.caption(
            "💡 **When to use:** Rapid edits to `Snakefile`, custom rule testing, or debugging notebook logic directly in the repository."
        )

    with tab_packaged:
        st.markdown("##### Packaged CLI Execution (`driver.sh`)")
        st.write("""
        Recommended for team and automated production runs. It utilizes the installed 
        `run-atw-diags` command (registered via `pip install -e .` in Module 8), which 
        automatically locates packaged workflow files and handles Jupyter kernel registration.
        """)

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

# Invokes the CLI entry point installed via 'pip install -e .'
run-atw-diags \\
    --case /home/a1r/git/atw/atw_diags/configs/atw_atmos_ts_monthly_sfc_ocean_updated_config.json \\
    --settings /home/a1r/git/atw/atw_diags/diagnostics/settings.json \\
    out_dir="/work/a1r/" -w $TMPDIR
""",
            language="bash",
        )

        st.caption(
            "💡 **When to use:** Production workloads and cluster-wide automated runs where the package is installed in the active environment."
        )

    # ── Job Control & Verification ───────────────────────────────────────
    st.markdown("---")
    st.subheader("2. Job Submission & Output Verification")

    st.write("Submit whichever driver script fits your current task:")
    st.code(
        """# For dev testing:
sbatch src/atw_diags/workflow/vanilla_driver.sh

# For packaged production:
sbatch src/atw_diags/workflow/driver.sh
""",
        language="bash",
    )

    st.write("Check queue status and inspect real-time log output:")
    st.code(
        """# 1. Check job state on allocated compute nodes
squeue -u $USER

# 2. Stream live logs (stdout/stderr combined)
tail -f /work/a1r/slurm_<JOB_ID>.out
""",
        language="bash",
    )

    st.write("**Where artifacts live upon completion:**")
    st.markdown("""
    * **`*_executed.ipynb`**: Contains cell-by-cell execution timings, outputs, and injected parameters (`config_path`, `out_dir`).
    * **Diagnostic Figures**: Output plots (e.g. `t_surf_final_replica.png`) saved to your specified `out_dir`.
    * **Slurm Output (`slurm_<JOB_ID>.out`)**: Records environment setup, node hostname, Snakemake step progression, and exit codes.
    """)

    # ── Knowledge Check ─────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Knowledge Check")

    q1 = st.radio(
        "1. Why is the `run-atw-diags` command available directly in the terminal within `driver.sh`?",
        [
            "Because we ran `pip install -e .` in Module 8, registering the script entry point into our Conda environment.",
            "Because Slurm automatically converts every Python script in the repository into a shell command.",
            "Because Snakemake compiles it into an executable binary on the fly.",
        ],
    )

    q2 = st.radio(
        "2. When would you prefer using `vanilla_driver.sh` over `driver.sh`?",
        [
            "When actively developing and testing edits in the local Snakefile or notebook without relying on package CLI wrappers.",
            "When submitting the final workflow for automated cluster-wide multi-user deployment.",
            "When running on nodes without any Conda installation.",
        ],
    )

    if st.button("Check Answers", type="primary"):
        c1 = (
            q1
            == "Because we ran `pip install -e .` in Module 8, registering the script entry point into our Conda environment."
        )
        c2 = (
            q2
            == "When actively developing and testing edits in the local Snakefile or notebook without relying on package CLI wrappers."
        )

        if c1 and c2:
            st.success("Correct! You're ready to submit and manage batch runs.")
        else:
            st.error("One or more answers need review. Check the tabs above and retry.")
