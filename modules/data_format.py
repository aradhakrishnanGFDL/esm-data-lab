
import streamlit as st


def run():
    st.title("Introduction to Data Formats")

    st.write(
        "Earth system models produce large amounts of data. "
        "They simulate variables such as temperature, rainfall, winds, "
        "and ocean conditions over many years. Scientists often run "
        "models multiple times to create an ensemble, helping them "
        "understand a range of possible Earth system outcomes."
    )

    st.info(
        "In this module, we introduce NetCDF, Zarr, and Icechunk, "
        "explore why chunking matters, and see how VirtualiZarr "
        "can help us work with existing NetCDF data."
    )

    # ── Step 1 ──────────────────────────────────────────────────────────────
    st.header("1. Understanding Earth system model data")

    st.write(
        "Imagine running an Earth system model three times. Each run "
        "is an ensemble member. Each member can contain many variables, "
        "time steps, and locations around the globe."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Ensemble member 1**")
        st.caption("One model run")
        st.write("Temperature")
        st.write("Rainfall")
        st.write("Wind")

    with col2:
        st.markdown("**Ensemble member 2**")
        st.caption("Another model run")
        st.write("Temperature")
        st.write("Rainfall")
        st.write("Wind")

    with col3:
        st.markdown("**Ensemble member 3**")
        st.caption("Another model run")
        st.write("Temperature")
        st.write("Rainfall")
        st.write("Wind")

    st.caption(
        "Each ensemble member may contain decades or centuries of "
        "data, across many variables and spatial locations."
    )

    st.write(
        "A temperature dataset, for example, might have three dimensions: "
        "time, latitude, and longitude. Adding more variables, longer "
        "simulations, and more ensemble members quickly increases "
        "the amount of data we need to store and analyse."
    )

    st.markdown("---")

    # ── Step 2 ──────────────────────────────────────────────────────────────
    st.header("2. NetCDF: a common format for scientific data")

    st.write(
        "NetCDF is widely used to store Earth system model output. "
        "A NetCDF file can contain multidimensional data along with "
        "useful information such as variable names, units, and coordinates."
    )

    st.write("For example, a file might contain daily temperature data:")

    st.code(
        """
temperature
    time: 365 days
    latitude: 180 points
    longitude: 360 points

units: K
        """.strip(),
        language="text",
    )

    st.caption(
        "The dimensions above are illustrative. K means kelvin, "
        "a unit of temperature."
    )

    st.write("A NetCDF file commonly has the extension `.nc`.")

    st.write("We can use Python's xarray library to open one:")

    st.code(
        """
import xarray as xr

ds = xr.open_dataset("temperature.nc")

print(ds)
print(ds["temperature"])
        """.strip(),
        language="python",
    )

    st.caption(
        "This example assumes that temperature.nc exists in your "
        "working directory. xarray helps us explore labelled scientific "
        "datasets without having to manage every array dimension manually."
    )

    st.markdown(
        "[NetCDF documentation](https://www.unidata.ucar.edu/software/netcdf/) "
        "| [xarray I/O guide](https://docs.xarray.dev/en/stable/user-guide/io.html)"
    )

    st.markdown("---")

    # ── Step 3 ──────────────────────────────────────────────────────────────
    st.header("3. Zarr: work with large datasets in smaller pieces")

    st.write(
        "Zarr is another format for storing multidimensional arrays. "
        "It is especially useful for large datasets and workflows that "
        "access data from cloud or object storage."
    )

    st.write(
        "One of its key ideas is **chunking**: dividing a large array "
        "into smaller blocks. This can make it easier to read only "
        "the data needed for a particular analysis."
    )

    st.subheader("What does chunking look like?")

    st.write(
        "Imagine a global temperature map. You only want to study "
        "a small region of the North Atlantic. You may not need to "
        "read every grid cell in the entire map."
    )

    st.write("The diagram below illustrates a large array divided into chunks.")

    # Illustrative chunk grid; highlighted blocks represent a selected region.
    for row_idx in range(4):
        cols = st.columns(8, gap="small")

        for col_idx, col in enumerate(cols):
            selected = (
                row_idx in (1, 2)
                and col_idx in (2, 3, 4)
            )

            with col:
                if selected:
                    st.markdown(
                        """
                        <div style="
                            background-color: #F4A261;
                            border: 1px solid white;
                            border-radius: 4px;
                            padding: 12px 0;
                            text-align: center;
                            color: #222222;
                            font-size: 11px;">
                            Selected
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <div style="
                            background-color: #D9EAF7;
                            border: 1px solid white;
                            border-radius: 4px;
                            padding: 12px 0;
                            text-align: center;
                            color: #23415A;
                            font-size: 11px;">
                            Chunk
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    st.caption(
        "Illustration only: highlighted chunks represent the region "
        "of interest. Actual chunk shapes and sizes depend on the dataset."
    )

    st.write(
        "Chunking can reduce unnecessary data access, but the benefit "
        "depends on how the data is organised. If chunks are poorly "
        "matched to the analysis, a request for a small region may "
        "still require reading much more data than expected."
    )

    st.write("Here is a simple example using xarray to open Zarr data:")

    st.code(
        """
import xarray as xr

ds = xr.open_zarr("temperature.zarr")

# Select a time period and geographic region
subset = ds["temperature"].sel(
    time=slice("2050-01-01", "2050-12-31"),
    latitude=slice(30, 50),
    longitude=slice(-80, -50),
)
        """.strip(),
        language="python",
    )

    st.caption(
        "This example assumes that the Zarr dataset contains the "
        "temperature variable and the requested coordinates. Coordinate "
        "ordering and time labels vary between datasets."
    )

    st.markdown(
        "[Official Zarr website](https://zarr.dev/) "
        "| [Zarr Python documentation](https://zarr.readthedocs.io/)"
    )

    with st.expander("Explore further: the Zarr Python library"):
        st.write(
            "The Zarr Python library lets us create, read, and update "
            "chunked arrays. You can use it directly or through libraries "
            "such as xarray."
        )

        st.write("For example, we can create a small array and store it as Zarr:")

        st.code(
            """
import numpy as np
import zarr

data = np.arange(100)

array = zarr.create_array(
    store="example.zarr",
    shape=data.shape,
    chunks=(20,),
    dtype=data.dtype,
    overwrite=True,
)

array[:] = data

print(array[20:30])
            """.strip(),
            language="python",
        )

        st.write(
            "The array contains 100 numbers, organised into chunks "
            "of 20. The final line requests just 10 numbers. Chunking "
            "allows the storage system to identify which pieces are "
            "needed for that request."
        )

        st.caption(
            "This example uses the Zarr Python 3 API and creates a local "
            "store. Check the installed Zarr version if you are using "
            "an existing course environment."
        )

        st.markdown(
            "[Zarr Python getting started guide]"
            "(https://zarr.readthedocs.io/en/stable/user-guide/)"
        )

    st.markdown("---")

    # ── Step 4 ──────────────────────────────────────────────────────────────
    st.header("4. Icechunk: keep track of data changes")

    st.write(
        "Imagine a research group working with a large collection "
        "of Earth system model output. Someone updates a dataset, "
        "but another researcher needs to reproduce an earlier analysis."
    )

    st.write(
        "Icechunk works with Zarr data and adds versioning and "
        "transactional updates. In simple terms, it helps researchers "
        "record changes, revisit earlier versions, and publish updates "
        "in a consistent way."
    )

    tab1, tab2 = st.tabs(
        ["Without versioning", "With Icechunk"]
    )

    with tab1:
        st.write(
            "If data changes over time, it can be difficult to know "
            "which version was used for an earlier result unless "
            "versions are managed separately."
        )

    with tab2:
        st.write(
            "Icechunk records changes through commits and snapshots. "
            "Researchers can refer to a particular version of the data "
            "rather than relying only on the latest state."
        )

    st.caption(
        "Icechunk is not simply another file format. It provides "
        "version management and coordinated updates for Zarr-based data."
    )

    st.markdown(
        "[Official Icechunk documentation](https://icechunk.io/en/latest/)"
    )

    st.markdown("---")

    # ── Step 5 ──────────────────────────────────────────────────────────────
    st.header("5. Did you know? VirtualiZarr")

    st.info(
        "You may be able to use existing NetCDF data in a Zarr-based "
        "workflow without first copying all of the underlying data."
    )

    st.write(
        "Scientific archives often contain thousands of NetCDF files. "
        "Converting every file into a new format can take time and "
        "require additional storage."
    )

    st.write(
        "VirtualiZarr can create virtual representations of supported "
        "existing datasets. Instead of copying all the data, it records "
        "references to the original data and presents it in a form that "
        "compatible Zarr-based tools can work with."
    )

    st.write("Think of it like a library catalogue:")

    st.markdown(
        """
        - The books stay on the original shelves.
        - The catalogue records where each book is stored.
        - You can organise and find the material without copying
          every book into a new building.
        """
    )

    st.caption(
        "Virtual representations are not full converted copies. "
        "Support depends on the source files, metadata, storage access, "
        "and operations performed by the tools."
    )

    st.markdown(
        "[Official VirtualiZarr documentation]"
        "(https://virtualizarr.readthedocs.io/en/stable/)"
    )

    st.markdown("---")

    # ── Step 6 ──────────────────────────────────────────────────────────────
    st.header("6. How do these tools fit together?")

    st.write(
        "These tools address different parts of working with large "
        "scientific datasets."
    )

    st.table(
        {
            "Tool": [
                "NetCDF",
                "Zarr",
                "Icechunk",
                "VirtualiZarr",
            ],
            "What it helps with": [
                "Storing scientific data and metadata",
                "Storing arrays in chunks for flexible access",
                "Tracking versions and coordinating data updates",
                "Representing existing data virtually for compatible workflows",
            ],
        }
    )

    st.write(
        "For Earth system research, these tools can help us manage "
        "large model outputs, explore multiple ensemble members, "
        "analyse selected regions and time periods, and make data "
        "workflows more reproducible."
    )

    st.markdown("---")

    # ── Task ────────────────────────────────────────────────────────────────
    st.header("Your turn")

    st.write(
        "Imagine you have 50 ensemble members, each containing "
        "100 years of daily global temperature data."
    )

    answer1 = st.radio(
        "1. You want to analyse one geographic region. Which Zarr "
        "feature can help limit unnecessary data access?",
        ["Version history", "Chunking", "File extensions"],
        index=None,
    )

    answer2 = st.radio(
        "2. Your team needs to revisit an earlier version of a shared "
        "Zarr dataset. Which tool can help?",
        ["NetCDF", "Icechunk", "A larger chunk size"],
        index=None,
    )

    answer3 = st.radio(
        "3. You have existing NetCDF files and want a virtual "
        "Zarr representation without copying all the underlying data. "
        "Which tool could help?",
        ["VirtualiZarr", "Icechunk alone", "A plotting library"],
        index=None,
    )

    if st.button("Check my answers"):
        if all(
            answer is not None
            for answer in (answer1, answer2, answer3)
        ):
            score = sum(
                [
                    answer1 == "Chunking",
                    answer2 == "Icechunk",
                    answer3 == "VirtualiZarr",
                ]
            )

            st.write(f"You got **{score} out of 3** correct.")

            if score == 3:
                st.success(
                    "Well done! You understand the main ideas."
                )
                st.balloons()
            else:
                st.info(
                    "Review the sections above and try again. "
                    "Remember: chunking helps organise data access, "
                    "Icechunk tracks versions, and VirtualiZarr creates "
                    "virtual representations of supported datasets."
                )
        else:
            st.warning("Please answer all three questions first.")

    st.markdown("---")
    st.caption(
        "Further reading: "
        "[NetCDF](https://www.unidata.ucar.edu/software/netcdf/) | "
        "[Zarr](https://zarr.dev/) | "
        "[Icechunk](https://icechunk.io/en/latest/) | "
        "[VirtualiZarr](https://virtualizarr.readthedocs.io/en/stable/)"
    )
