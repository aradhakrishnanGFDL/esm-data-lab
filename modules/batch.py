import streamlit as st

def run():
    st.title("Module 8: Running Batch Jobs with Slurm")
    st.write("""
    In Module 7, you ran notebooks interactively in VSCode. For data-intensive 
    production runs, submit your work as a **batch job** using Slurm so it runs headlessly 
    on GFDL cluster nodes.
    """)

    st.info("Goal: Learn how Snakemake executes notebooks and submit your first Slurm job using `driver.sh`.")

    # ── Jargon Buster ────────────────────────────────────────────────────
    with st.expander("📚 Jargon Buster (Snakemake, Papermill, CLI)"):
        st.markdown("""
        * **Snakemake**: Workflow manager that runs data pipeline steps automatically.
        * **Papermill**: Tool used by Snakemake to execute Jupyter notebooks headlessly and inject input parameters.
        * **Headless Execution**: Running code in the background without needing a terminal or GUI open.
        * **CLI**: Command line shortcut (like `run-atw-diags`) that executes Python scripts with clean arguments.
        """)

    # ── Step 1 ───────────────────────────────────────────────────────────
    st.markdown("#### 1. Method A: Direct Approach (`vanilla_driver.sh`)")
    st.write("`vanilla_driver.sh` runs raw Snakemake directly:")
    st.code("cat src/atw_diags/workflow/vanilla_driver.sh", language="bash")

    st.code("""
#!/bin/bash
set -e
cd /home/a1r/git/atw/atw_diags
export ATW_NB_DIR="/home/a1r/git/atw/atw_diags/src/atw_diags/notebooks"

source $(conda info --base)/etc/profile.d/conda.sh
conda activate snakemake-env

snakemake -s src/atw_diags/workflow/Snakefile --cores 4 --use-conda --forceall
""", language="bash")

    st.warning("**Drawbacks:** Requires hardcoded working directories, manual environment export variables, and lacks easy dynamic config passing.")

    # ── Step 2 ───────────────────────────────────────────────────────────
    st.markdown("#### 2. Method B: Package Approach (`driver.sh`)")
    st.write("To solve these path and config issues, `driver.sh` uses the installed `pip` package CLI (`run-atw-diags`):")
    st.code("cat src/atw_diags/workflow/driver.sh", language="bash")

    st.code("""
#!/bin/bash
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

run-atw-diags \\
    --case /home/a1r/git/atw/configs/atw_atmos_ts_monthly_sfc_ocean_updated_config.json \\
    --settings /home/a1r/git/atw/configs/settings.json \\
    out_dir="/work/a1r/" -w $TMPDIR
""", language="bash")

    st.info("""
    **What `driver.sh` resolves behind the scenes (`runner.py`):**
    * Automatically finds the internal `Snakefile` inside the Conda environment package.
    * Registers the Jupyter kernel for Papermill automatically.
    * Allows passing custom JSON configs directly from the command line.
    """)

    # ── Step 3 ───────────────────────────────────────────────────────────
    st.markdown("#### 3. Submit and Monitor")
    st.write("Submit the job from your repository root:")
    st.code("sbatch src/atw_diags/workflow/driver.sh", language="bash")

    st.write("Check queue status and stream live logs:")
    st.code("squeue -u $USER\ntail -f /work/a1r/slurm_<JOB_ID>.out", language="bash")

    # ── Reflection Quiz ──────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Quiz")

    q1 = st.radio(
        "1. What main issue in `vanilla_driver.sh` does `driver.sh` resolve?",
        [
            "It eliminates hardcoded repository paths and manual notebook directory exports.",
            "It runs the pipeline without a Conda environment.",
            "It allows jobs to run without memory.",
        ]
    )

    q2 = st.radio(
        "2. What does Papermill do inside the Snakemake workflow?",
        [
            "Allocates Slurm nodes.",
            "Executes Jupyter notebooks headlessly and passes parameters into cells.",
            "Compiles Python into C++.",
        ]
    )

    if st.button("Check Answers"):
        if (
            q1 == "It eliminates hardcoded repository paths and manual notebook directory exports."
            and q2 == "Executes Jupyter notebooks headlessly and passes parameters into cells."
        ):
            st.success("Correct!")
        else:
            st.error("Some answers were incorrect. Review the steps above.")

    # ── Task ─────────────────────────────────────────────────────────────
    st.markdown("---")
    completed = st.checkbox("I submitted `driver.sh` via sbatch and checked logs with `tail -f`")
    if completed:
        job_id = st.text_input("Enter your Slurm Job ID:")
        if job_id:
            st.success(f"Job {job_id} tracked!")
            st.balloons()
