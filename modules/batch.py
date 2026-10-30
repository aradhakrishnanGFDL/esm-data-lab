import streamlit as st

def run():
    st.title("Module 8: Running Batch Jobs with Slurm")
    st.write("""
    In Module 7, you ran the diagnostic notebook interactively inside VSCode. 
    While VSCode is ideal for active code development and debugging, data and time-intensive diagnostic runs 
    take significant resources. For full production runs, submit your work 
    as a **batch job** using Slurm so it runs headlessly on GFDL cluster nodes. If you're from a different organization, please consult your organizational practices for submitting 
    batch jobs.
    """)
    
    st.info("By the end of this module, you will submit your first batch job using `driver.sh` and learn how to track its execution under the hood.")

    # ── Step 1 ───────────────────────────────────────────────────────────
    st.markdown("#### 1. Locate `driver.sh` in your repo")
    st.write("Open your terminal on the GFDL analysis machine, navigate to your repository, and check the workflow directory:")
    st.code("cd ~/git/atw\nls src/atw_diags/workflow/driver.sh", language="bash")
    st.write("Inspect the contents of the batch driver script:")
    st.code("cat src/atw_diags/workflow/driver.sh", language="bash")

    st.subheader("Understanding the `driver.sh` script")
    st.code("""
#!/bin/bash
#SBATCH --job-name=atw_diags
#SBATCH --nodelist=pp339,pp340,pp341,pp342,pp343
#SBATCH --output=/work/a1r/slurm_%j.out
#SBATCH --error=/work/a1r/slurm_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --partition=batch

# 1. Ensure the module/conda environment is loaded
source /etc/profile.d/modules.sh 2>/dev/null || true
source ~/.bashrc
source $(conda info --base)/etc/profile.d/conda.sh

conda activate spear-analysis-pip

# 2. Run the diagnostics CLI command
run-atw-diags \\
    --case /home/a1r/git/atw/configs/atw_atmos_ts_monthly_sfc_ocean_updated_config.json \\
    --settings /home/a1r/git/atw/configs/settings.json \\
    out_dir="/work/a1r/" -w $TMPDIR
""", language="bash")

    # ── Step 2 ───────────────────────────────────────────────────────────
    st.markdown("#### 2. What is happening under the hood?")
    st.write("""
    `driver.sh` acts as the bridge between the Slurm cluster scheduler and your Python environment.
    When you execute this script, two distinct layers work together:
    """)

    st.subheader("Layer A: Slurm Allocation (The `#SBATCH` directives)")
    st.write("""
    - Requests 1 compute node with 4 CPUs and 32GB memory for up to 4 hours.
    - Redirects standard output and errors into `/work/a1r/slurm_<JOB_ID>.out` (where `%j` is replaced by the Slurm Job ID).
    """)

    st.subheader("Layer B: Python Execution (`run-atw-diags`)")
    st.write("""
    Notice that `driver.sh` calls `run-atw-diags`. Under the hood, this executable command:
    1. **Calls `runner.py`**: A Python CLI wrapper installed inside your `spear-analysis-pip` conda environment.
    2. **Locates internal resources**: Automatically finds the packaged `Snakefile` inside `site-packages` so you don't have to specify hardcoded relative paths.
    3. **Registers the Jupyter kernel**: Automatically registers the active environment as the `atw-diags` kernel so **Papermill** can execute your notebook automatically.
    4. **Triggers Snakemake**: Passes your JSON configuration parameters into Snakemake to execute the diagnostic pipeline steps.
    """)

    st.info("Tip: Because `run-atw-diags` handles path finding automatically, you can submit `sbatch src/atw_diags/workflow/driver.sh` from any directory on the workstation without file-not-found errors.")

    # ── Step 3 ───────────────────────────────────────────────────────────
    st.markdown("#### 3. Submit your job to Slurm")
    st.write("From your repository root (`~/git/atw`), submit your job to the cluster queue using `sbatch`:")
    st.code("sbatch src/atw_diags/workflow/driver.sh", language="bash")
    st.write("Slurm will return a response with your assigned Job ID, for example:")
    st.code("Submitted batch job 1234567", language="bash")

    # ── Step 4 ───────────────────────────────────────────────────────────
    st.markdown("#### 4. Monitor your running job")
    st.write("You can check the status of your queued or running jobs at any time:")
    st.code("squeue -
