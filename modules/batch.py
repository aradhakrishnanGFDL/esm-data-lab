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
