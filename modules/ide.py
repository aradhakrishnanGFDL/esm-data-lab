import streamlit as st

def run():
    st.title("Module 7: Running a Jupyter Notebook")

    st.write("This module walks you through running a Jupyter notebook in VSCode or JupyterLab.")

    tab_vscode, tab_jupyter = st.tabs(["VSCode", "JupyterLab"])

    with tab_vscode:
        st.subheader("Connecting VSCode to your GFDL workstation")
        st.write("""
        These instructions cover connecting VSCode from your local laptop to your GFDL workstation. 
        The same steps apply if you are working directly on a GFDL workstation — 
        just generate the SSH keys and edit the `~/.ssh/config` from the workstation instead of your laptop.
        """)

        # ── Step 1 ───────────────────────────────────────────────────────────
        st.markdown("#### 1. Install VSCode")
        st.write("If you don't have VSCode installed, download it from:")
        st.code("https://code.visualstudio.com/download", language="bash")

        # ── Step 2 ───────────────────────────────────────────────────────────
        st.markdown("#### 2. Install the Remote SSH extension")
        st.write("In VSCode, open the Extensions panel (`Ctrl+Shift+X`) and search for:")
        st.code("Remote - SSH", language="bash")
        st.write("Install it.")

        # ── Step 3 ───────────────────────────────────────────────────────────
        st.markdown("#### 3. One-time SSH setup")
        st.write("This only needs to be done once.")

        st.subheader("Generate an SSH key")
        st.write("Open a terminal on your local machine (or GFDL workstation) and run:")
        st.code("ssh-keygen", language="bash")
        st.write("Hit Enter to accept all defaults. Do not set a password when prompted.")

        st.subheader("Copy your public key to the analysis machine")
        st.write("Open a second terminal and SSH into analysis. In your first terminal, print your public key:")
        st.code("cd ~/.ssh\ncat id_rsa.pub", language="bash")
        st.write("Copy the entire output. In your analysis terminal, run:")
        st.code("echo <paste copied key here> >> ~/.ssh/authorized_keys", language="bash")
        st.write("Exit both terminals.")

        st.subheader("Edit your SSH config file")
        st.write("When you SSH into analysis, you will see something like this before picking a node:")
        st.code("""Enter a hostname, or a unique portion of a hostname []: an200
Local port 44088 forwarded to remote host.
Remote port 54088 forwarded to local host.""", language="bash")
        st.write("Open your SSH config file and add the following, using those port numbers:")
        st.code("nano ~/.ssh/config", language="bash")
        st.write("For example:")
        st.code("""Host analysis
    HostName               analysis-rsa.princeton.rdhpcs.noaa.gov
    User                   First.Last
    ControlMaster          auto
    LocalForward           44088 localhost:44088
    RemoteForward          54088 localhost:22""", language="bash")
        st.write("Then add a second entry. The name `local_analysis` is a label that tells VSCode to connect via the tunnel established when you SSH into analysis:")
        st.code("""host local_analysis
    HostName               localhost
    Port                   44088
    User                   First.Last
    PasswordAuthentication yes""", language="bash")
        st.write("Save and close the file. In nano: `Ctrl+O` to save, `Ctrl+X` to exit.")

        # ── Step 4 ───────────────────────────────────────────────────────────
        st.markdown("#### 4. Connect to your workstation")
        st.write("Each time you want to connect, open a terminal and SSH into analysis first. Keep this window open and minimized — VSCode routes through this tunnel.")
        st.write("Then open VSCode. There are two ways to connect:")

        st.subheader("Option 1: Remote window icon")
        st.write("Click the remote window icon in the bottom left corner, select **Connect to Host**, and choose `local_analysis` from the list.")

        st.subheader("Option 2: Remote Explorer")
        st.write("Open the Remote Explorer panel from the left sidebar, find `local_analysis` under SSH targets, and click the connect icon next to it.")

        st.image("assets/vscode_remote.png", caption="Left: Remote Explorer panel. Bottom left: click the remote window icon to connect.")
        st.write("VSCode will connect to your workstation without asking for a password.")
        st.info("Tip: Once connected, the bottom left corner changes to show `SSH: local_analysis` confirming you are on the remote machine.")

        # ── Step 5 ───────────────────────────────────────────────────────────
        st.markdown("#### 5. Open your repo folder")
        st.write("Once connected, go to **File → Open Folder** and navigate to your repo on the workstation, for example `atw_diags`.")

        # ── Step 6 ───────────────────────────────────────────────────────────
        st.markdown("#### 6. Select your Python interpreter")
        st.write("""
        VSCode needs to know which Python environment to use. 
        Open the Command Palette by pressing `Ctrl+Shift+P` — this opens a search bar at the top of VSCode. 
        Type `Python: Select Interpreter` and select your environment from the list.
        """)
        st.info("Refer to Module 6 to set up your conda or pixi environment before selecting it here.")

        # ── Step 7 ───────────────────────────────────────────────────────────
        st.markdown("#### 7. Open a Jupyter notebook")
        st.write("Install the Jupyter extension in VSCode if you haven't already — search for `Jupyter` in the Extensions panel (`Ctrl+Shift+X`).")
        st.write("Then open any `.ipynb` file from your repo folder.")
        st.write("""
        When prompted to select a kernel, choose your conda or pixi environment. 
        See Module 6 for instructions on setting up your environment — 
        conda and pixi are covered in separate tabs there.
        """)
        st.write("For example, if you cloned `atw_diags` in Module 1, open:")
        st.code("src/atw_diags/notebooks/atw_atmos_ts_monthly_sfc_ocean_updated.ipynb", language="bash")
        st.write("Or navigate to it in VSCode via **File → Open File** from within your repo folder.")
        st.subheader("Test without a notebook")
        st.write("In a notebook cell, run:")
        st.code("import xarray as xr\nprint(xr.__version__)", language="python")
        st.write("If it runs without errors, you are ready to develop.")


        st.subheader("Running cells in a notebook")
        st.write("There are a few ways to run a cell in VSCode:")
        st.write("- **Run a single cell:** Click the play button to the left of the cell, or press `Shift+Enter`")
        st.write("- **Run all cells:** Click **Run All** at the top of the notebook")
        st.write("- **Run cells above:** Right click a cell and select **Run All Above**")
        st.info("Tip: `Shift+Enter` runs the current cell and moves to the next one — useful for stepping through a notebook.")

        # ── Task ─────────────────────────────────────────────────────────────
        st.markdown("---")
        st.write("**Your turn:** Connect to your workstation and run the test cell above.")
        completed = st.checkbox("I connected to my workstation and ran a notebook in VSCode")
        if completed:
            st.success("You are set up and ready to develop on your GFDL workstation.")

    with tab_jupyter:
        st.subheader("Running a Jupyter notebook in JupyterLab")
        st.write("Coming soon.")

    st.markdown("---")
    st.write("Next: Module 8 — More IDE tips and tricks")