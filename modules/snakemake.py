import streamlit as st

def run():
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
    st.header("2. What is Papermill & How to Tag Notebooks")

    st.write("""
    **Papermill** is a command-line tool that executes Jupyter notebooks automatically in the background without opening a browser interface.

    * **Headless Execution:** Runs notebooks top-to-bottom on compute nodes.
    * **Parameter Injection:** Overrides default variables (e.g., case names, file paths) at runtime.
    * **Output Preservation:** Saves a rendered notebook with all generated plots and cell logs.
    """)

    # ── Sub-step: GUI Instructions for Students ──
    st.subheader("How to Add the `parameters` Tag in VS Code")
    st.write("Before Papermill can pass runtime values to a notebook, you must designate the cell containing your default variables as the parameters cell:")
    col_gui1, col_gui2 = st.columns([2, 3])
    with col_gui1:
        st.markdown("""
        **Tagging Steps:**
        1. Open your `.ipynb` notebook file in VS Code.
        2. Click on the cell containing your default parameter variables.
        3. Click the **'More Actions' (•••)** button on the top-right toolbar of the cell frame.
        4. Select **'Mark Cell as Parameters'** from the dropdown menu.
        5. Verify that the **`parameters`** tag appears at the bottom-left corner of that cell's frame.
        """)
        
        st.info(" **Alternatively:** You can also click the `+ Tag` button at the bottom-left of the cell and type `parameters` manually!")
        

    from pathlib import Path
    from PIL import Image
        
     try:

            # Point to project root (/mount/src/esm-data-lab/)
            PROJECT_ROOT = Path(__file__).resolve().parent.parent

            # Path to the root assets folder
            IMAGE_PATH = PROJECT_ROOT / "assets" / "papermill_tagging.jpeg"
            img = Image.open(IMAGE_PATH)
            st.image(img, caption="Visual Guide: Marking a cell as parameters using VS Code cell actions.", use_container_width=True)
      except Exception as e:
            st.warning(f"Could not load Image asset: verify assets/papermill_tagging.jpeg exists. Error: {e}")
          
    st.subheader("How Parameter Injection Works at Runtime")
    st.write("When Papermill runs, it leaves your original tagged cell untouched and automatically inserts a new cell directly below it with the updated values:")

    col_cell1, col_cell2 = st.columns(2)
    with col_cell1:
        st.subheader("Original Cell (Tagged: `parameters`)")
        st.code("""
# Default parameters inside notebook
OUTPUT_DIR = None
config_path = None
settings_path = None
""", language="python")

    with col_cell2:
        st.subheader("Injected Cell Added by Papermill")
        st.code("""
# Injected cell added automatically below parameters cell
OUTPUT_DIR = "/work/jill.bo/diags/out"
config_path = "/nbhome/jill.bo/git/atw_diags/configs/settings.json"
settings_path = "/nbhome/jill.bo/git/atw_diags/configs/settings.json"
""", language="python")

    st.caption("Note: Because Python executes cells top-to-bottom, the injected variables below automatically override your initial defaults for the remainder of the notebook execution.")
    

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
