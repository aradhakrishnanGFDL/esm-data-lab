import streamlit as st


def run():
    st.title("Scientific Data Formats: The Basics")
    st.write(
        "How do large volumes of earth system model data is structured? From traditional data formats to scalable, chunked data formats (efficient, performant) in platforms that bring analysis to the data (no-downloads) - this module will give a basic background on all this. 
        Enjoy learning!"
        )
    )
    st.info(
        "**In this module:** meet NetCDF, Zarr, Icechunk, and VirtualiZarr. "
        "No previous experience with these formats is needed."
    )

    # 1. Start with the data
    st.header("1. What does scientific data look like?")
    st.write(
        "Imagine a researcher wants to study temperature around the "
        "world over many years."
    )
    st.code("temperature(time, latitude, longitude)", language="text")
    st.markdown("""
    - **Time:** when was it measured?
    - **Latitude and longitude:** where was it measured?
    - **Temperature:** what value was measured?
    """)
    with st.expander("One useful extra: metadata"):
        st.write(
            "Metadata is information *about* the data. Think of a label on a "
            "container: it tells you what is inside and helps you interpret it."
        )
        st.code(
            'variable: temperature\nunits: "K"\nlong_name: "Near-surface air temperature"',
            language="yaml",
        )
        st.caption(
            "Variables hold values. Dimensions describe the array's axes. "
            "Attributes describe a variable or the dataset as a whole."
        )

    # ── A quick analogy: Rubik's Cube ─────────────────────────────
    st.header("A quick analogy: a Rubik's Cube")

    st.write("""
    Imagine a Rubik's Cube with many small cubes arranged in layers.
    Scientific data can also be organized across multiple dimensions.
    """)

    st.markdown("""
    - **Data cube:** The entire Rubik's Cube represents the full dataset,
      with dimensions such as *time*, *latitude*, and *longitude*.
    - **Zarr chunks:** One or more small cubes represent a chunk of data
      stored and retrieved together.
    - **Object store:** A storage space holding these chunks as separate
      objects, each of which can be retrieved when needed. This storage space can be platforms such as commercial or institutional non-commercial research cloud. It's the object store interface that is important here!
    """)

    st.info(
        "Instead of downloading the entire dataset, we can retrieve only "
        "the Zarr chunks needed for our analysis."
    )
    # 2. NetCDF
    st.header("2. NetCDF: a labeled notebook")
    st.write(
        "Think of NetCDF as a scientific notebook: it stores data together "
        "with labels that explain what the values mean."
    )
    st.markdown("""
    - Often stored as a file ending in **`.nc`** or **`.nc4`**.
    - Can store multidimensional arrays, dimensions, and metadata.
    - Widely used in climate, weather, ocean, and other sciences.
    """)
    st.info(
        "**Self-describing:** the file can carry information about its "
        "variables, dimensions, and attributes instead of leaving you to guess "
        "what the numbers mean."
    )

    # 3. Zarr
    st.header("3. Zarr: a big dataset split into smaller boxes")
    st.write(
        "Imagine the climate dataset is a huge set of boxes. Zarr organizes "
        "array data into smaller pieces called **chunks**."
    )
    st.write(
        "If you only need temperature for one region and one month, you may "
        "only need some chunks—not the entire dataset."
    )
    st.success(
        "**Main idea:** chunked storage can make partial reads and parallel "
        "work more practical, especially when data is stored remotely."
    )
    st.caption(
        "Zarr commonly uses a directory or object-store prefix containing "
        "metadata and chunk objects, rather than one monolithic `.nc` file."
    )

    # 4. Icechunk
    st.header("4. Icechunk: keep track of changes")
    st.write(
        "Think of version history in a shared document: you can manage updates "
        "and keep track of different states."
    )
    st.write(
        "**Icechunk** helps manage versions and transactional changes to "
        "chunked scientific datasets, especially Zarr data."
    )
    st.caption(
        "Quick distinction: Zarr organizes chunked arrays; Icechunk helps "
        "manage changes and versions of chunked data."
    )

    # 5. VirtualiZarr
    st.header("5. VirtualiZarr: a map to data that already exists")
    st.write(
        "Imagine making a library catalog without moving all the books. The "
        "catalog points you to the books where they already live."
    )
    st.write(
        "**VirtualiZarr** can create virtual references to supported existing "
        "NetCDF data, allowing compatible tools to work with a Zarr-like view "
        "without rewriting all the underlying array data into Zarr chunks."
    )
    st.warning(
        "Virtual references are not a new copy of the data. The original files "
        "must still be available, and their existing layout may affect speed."
    )

    # 6. Growing data
    st.header("6. Why does this matter for big data?")
    st.write(
        "Imagine **30 earth-system-model ensemble members**, each producing daily "
        "data for **100 years**. Add more variables and experiments, and the "
        "collection can grow to terabytes or more."
    )
    st.markdown("""
    - **Ensemble members** are related model runs, such as runs with different
      initial conditions.
    - Downloading every file to every laptop may be impractical.
    - Instead, scientists often **bring analysis to the data**: run computation
      near the storage and read only what is needed.
    """)
    with st.expander("Where can scientific data live?"):
        st.markdown("""
        - **HPC:** high-performance computing systems, often with shared or
          parallel filesystems.
        - **Institutional or research cloud:** storage and computing managed by
          a research organization. Note that this can also provide object store access!
        - **Commercial cloud:** services that commonly provide object storage
          through network APIs.

        The same general ideas—data layout, chunking, and moving less data—
        matter in all these settings, though tools and performance differ.
        """)

    # Optional deeper dive
    with st.expander("Curious? Chunking, manifests, and performance"):
        st.markdown("""
        **A manifest is like a contents page.** It can describe where data
        pieces live. A virtual reference may include a source file, a byte
        offset, and the length of a piece of data.

        Keeping references separate from data can help tools find chunks
        without reading every value. Different workers may access different
        chunks in parallel.

        **Chunk size matters.** Very large chunks can make small selections read
        more data than needed. Tiny chunks can create many requests and metadata
        overhead.

        There is no single perfect chunk layout. Choose chunks based on how
        people will analyze the data, then test representative workloads.
        “Cloud-optimized” does not mean every analysis will be fast.
        """)

    # 7. Tiny Xarray example
    st.header("7. A tiny example with Xarray")
    st.write(
        "Xarray helps work with labeled scientific arrays. You do not need to "
        "learn the code here; just notice how a variable can be selected."
    )
    st.code(
        'import xarray as xr\n\nds = xr.open_dataset("sample.nc")\nprint(ds["temperature"])',
        language="python",
    )

    # 8. Quiz
    st.header("8. Quick quiz")
    q1 = st.radio(
        "A scientist wants a familiar scientific file that stores data and "
        "descriptive metadata. Which is a common choice?",
        ["NetCDF", "A screenshot", "A plain list of unlabeled numbers"],
        index=None, key="bite_q1",
    )
    q2 = st.radio(
        "You only need a small part of a very large array. What can help avoid "
        "reading the whole dataset?",
        ["Chunks", "A longer filename", "More global attributes"],
        index=None, key="bite_q2",
    )
    q3 = st.radio(
        "You have existing NetCDF files and want virtual references rather than "
        "rewriting all the array data. Which tool is relevant?",
        ["VirtualiZarr", "CF conventions", "A text editor"],
        index=None, key="bite_q3",
    )
    q4 = st.radio(
        "Which statement best describes Icechunk?",
        [
            "It helps manage versions and changes to chunked datasets",
            "It is a unit used to measure temperature",
            "It replaces the need for metadata",
        ],
        index=None, key="bite_q4",
    )

    if st.button("Check my answers"):
        answers = [
            (q1, "NetCDF", "NetCDF commonly stores scientific arrays with metadata."),
            (q2, "Chunks", "Chunks let tools access selected pieces of an array."),
            (
                q3, "VirtualiZarr",
                "VirtualiZarr can reference supported existing data without rewriting all values.",
            ),
            (
                q4, "It helps manage versions and changes to chunked datasets",
                "Icechunk helps manage changes and versions of chunked data.",
            ),
        ]
        score = 0
        for selected, correct, explanation in answers:
            if selected == correct:
                score += 1
                st.success(f"Correct! {explanation}")
            elif selected is None:
                st.info(f"Not answered. Correct answer: **{correct}**. {explanation}")
            else:
                st.warning(f"Correct answer: **{correct}**. {explanation}")
        st.write(f"**Your score: {score} / {len(answers)}**")

    st.header("Want to learn more?")
    st.markdown("""
    - [Unidata: NetCDF data model](https://docs.unidata.ucar.edu/netcdf-c/current/netcdf_data_model.html)
    - [CF conventions](https://cfconventions.org/)
    - [Xarray documentation](https://docs.xarray.dev/)
    - [Zarr documentation](https://zarr.readthedocs.io/)
    - [Icechunk documentation](https://icechunk.io/en/stable/)
    - [VirtualiZarr documentation](https://virtualizarr.readthedocs.io/en/stable/)
    """)

    st.markdown("### Reflect")
    st.info("Your reflection is not saved.")
    st.radio(
        "How confident do you feel about the basic differences between these tools?",
        ["Still learning", "Getting there", "Ready to explain the basics"],
        index=None, key="bite_reflection",
    )
    st.text_area(
        "What is one idea you want to remember?",
        placeholder="For example: chunks can help me read only the data I need...",
        key="bite_takeaway",
    )
