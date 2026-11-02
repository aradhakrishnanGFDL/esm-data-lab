import streamlit as st

def run_module_snakemake_papermill_slurm():
    st.title("Module 8.5: Workflow Automation with Snakemake, Papermill, and Slurm")

    # ── Learning Objectives & Scope ─────────────────────────────────────
    st.info("""
    **What you will learn in this module:**
    * How **Papermill** runs Jupyter notebooks automatically without needing a browser.
    * How **Snakemake** coordinates workflow steps and output files.
    * How **Slurm** schedules jobs on cluster compute nodes.
    
    *Note: Detailed batch script configuration (`driver.sh`) and advanced job management will be covered in Module 9.*
    """)

    # ── 1. The Core Components ──────────────────────────────────────────
    st.header("1. Core Components")

    st.write("""
    Running diagnostics automatically requires three complementary tools:
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Papermill")
        st.write("""
        Executes Jupyter notebooks automatically in the background and passes custom settings directly into notebook cells.
        """)

    with col2:
        st.subheader("Snakemake")
        st.write("""
        Tracks workflow rules and dependencies, making sure steps run in the correct order.
        """)

    with col3:
        st.subheader("Slurm")
        st.write("""
        Allocates cluster compute resources (nodes, CPUs, memory) to run tasks in the queue.
        """)

    # ── 2. What is Papermill? ───────────────────────────────────────────
    st.header("2. What is Papermill?")

    st.write("""
    **Papermill** is a command-line tool that executes Jupyter notebooks without opening a web browser.

    * **Headless Execution:** Runs notebooks in the background from top to bottom.
    * **Parameter Injection:** Passes runtime values (like dataset names or output paths) into a specific notebook cell.
    * **Saved Outputs:** Saves a completed copy of the notebook containing all cell outputs and generated plots.
    """)

    st.subheader("How Parameter Injection Works")
    st.write("Tag a cell in your notebook as `parameters`. When Papermill runs, it inserts a new cell below it with your custom runtime values:")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Notebook Cell (tagged: `parameters`)")
        st.code("""
# Default parameters inside notebook
case_name = "default_case"
out_dir = "/tmp/output"
""", language="python")

    with col2:
        st.subheader("Values Injected by Papermill at Runtime")
        st.code("""
# Injected values added automatically
case_name = "spear_atmos_ts_monthly"
out_dir = "/work/jill.bo/diags/out"
""", language="python")

    # ── 3. How Snakemake Works ──────────────────────────────────────────
    st.header("3. How Snakemake Coordinates Execution")

    st.write("Inside `src/atw_diags/workflow/Snakefile`, Snakemake defines rules that invoke Papermill with dynamic parameters:")

    st.code("""
rule run_diagnostic_notebook:
    input:
        config = "configs/settings.json"
    output:
        notebook = "{out_dir}/executed_diag_{case_name}.ipynb"
    params:
        case = "{case_name}",
        out_dir = "{out_dir}"
    shell:
        \"\"\"
        papermill src/atw_diags/notebooks/diagnostic_template.ipynb \\
                  {output.notebook} \\
                  -p case_name {params.case} \\
                  -p out_dir {params.out_dir}
        \"\"\"
""", language="python")

    # ── 4. Hands-On Test ────────────────────────────────────────────────
    st.header("4. Hands-On: Snakemake Dry-Run")

    st.markdown("""
    Run these commands in your GFDL cluster terminal to test your environment and preview workflow steps:
    """)

    st.code("""
# 1. Navigate to your cloned repository and activate your environment
cd /nbhome/jill.bo/git/atw_diags
conda activate spear-analysis

# 2. Perform a Snakemake dry-run (-n) to preview steps without running them
snakemake -s src/atw_diags/workflow/Snakefile -n
""", language="bash")

    # ── 5. Review Questions ─────────────────────────────────────────────
    st.markdown("---")
    st.subheader("Review Questions")

    q1 = st.radio(
        "1. What is the main purpose of Papermill?",
        [
            "It runs Jupyter notebooks automatically in the background and injects parameters into tagged cells.",
            "It formats matplotlib plot colors.",
            "It manages user passwords on the cluster.",
            "It converts Python code into shell scripts.",
        ]
    )

    q2 = st.radio(
        "2. What is the role of Snakemake in this setup?",
        [
            "It installs Python packages.",
            "It manages workflow steps, rule order, and output targets.",
            "It opens JupyterLab in your browser.",
            "It deletes old output files automatically.",
        ]
    )

    if st.button("Check Answers"):
        if (
            q1 == "It runs Jupyter notebooks automatically in the background and injects parameters into tagged cells."
            and q2 == "It manages workflow steps, rule order, and output targets."
        ):
            st.success("Correct. In Module 9, we will submit this setup to the Slurm queue.")
        else:
            st.error("Incorrect. Please review the material above.")
