import streamlit as st

def run():
    st.title("CIMES Summer Internship 2026")

    st.markdown("""
        <style>
        [data-baseweb="select"] input {
            pointer-events: none !important;
            caret-color: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)

    subtopic = st.selectbox("Choose a topic", [
        "Overview",
        "1. Jupyter Notebook",
        "2. Environments",
        "3. Python Packages",
        "4. Visual Studio Code",
        "5. Linux Operating Systems",
        "6. Shell Scripts",
        "7. Containers",
        "8. GitHub Actions and Workflow Automation",
        "9. APIs and AI Integration",
        "10. Globus",
        "11. DOI/DOI Policy",
    ])

    if subtopic == "Overview":
        st.header("Overview")
        st.markdown("""
- **Week 1 (June 8th to June 12th):** Goal
- **Week 2 (June 15th to June 19th):** Goal
- **Week 3 (June 22nd to June 26th):** Goal
- **Week 4 (June 29th to July 3rd):** Goal
- **Week 5 (July 6th to July 10th):** Goal
- **Week 6 (July 13th to July 17th):** Goal
- **Week 7 (July 20th to July 24th):** Goal
- **Week 8 (July 27th to July 31st):** Goal
- **Week 9 (August 3rd to August 7th):** Presentation Prep and Wrapping Up!
        """)

    elif subtopic == "1. Jupyter Notebook":
        st.header("1. Jupyter Notebook")
        st.write("Coming soon.")

    elif subtopic == "2. Environments":
        st.header("2. Environments")
        st.write("Coming soon.")

    elif subtopic == "3. Python Packages":
        st.header("3. Python Packages")
        st.write("Coming soon.")

    elif subtopic == "4. Visual Studio Code":
        st.header("4. Visual Studio Code")
        st.write("Coming soon.")

    elif subtopic == "5. Linux Operating Systems":
        st.header("5. Linux Operating Systems")
        st.write("Coming soon.")

    elif subtopic == "6. Shell Scripts":
        st.header("6. Shell Scripts")
        st.write("Coming soon.")

    elif subtopic == "7. Containers":
        st.header("7. Containers")
        st.write("Coming soon.")

    elif subtopic == "8. GitHub Actions and Workflow Automation":
        st.header("8. GitHub Actions and Workflow Automation")
        st.write("Coming soon.")

    elif subtopic == "9. APIs and AI Integration":
        st.header("9. APIs and AI Integration")
        st.write("Coming soon.")

    elif subtopic == "10. Globus":
        st.header("10. Globus")
        st.write("Coming soon.")

    elif subtopic == "11. DOI/DOI Policy":
        st.header("11. DOI/DOI Policy")
        st.write("Coming soon.")
