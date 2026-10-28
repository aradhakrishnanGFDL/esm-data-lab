import streamlit as st


DONE_HTML = """
<style>
  body { margin: 0; background: transparent; }
  @keyframes fadein {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .msg {
    font-family: sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #2e7d32;
    animation: fadein 0.8s ease forwards;
    opacity: 0;
    padding: 12px 0;
  }
</style>
<div class="msg">🌍 You're reading data like a pro!</div>
"""


def run():
    st.title("Accessing Data with xarray")
    st.write("""
        xarray is a Python library built for working with labeled, multi-dimensional data —
        exactly the kind you find in climate and earth science datasets.
        By the end of this module you'll be able to open a single NetCDF file and
        a collection of files as one dataset.
    """)
    st.info("Make sure xarray is installed: `pip install xarray`")

    # ── Step 1 ───────────────────────────────────────────────────────────────
    st.header("1. What is xarray?")
    st.write("""
        Think of xarray like a smarter NumPy array — it knows what its dimensions mean.
        Instead of `data[0, 3, 5]` you can write `data.sel(time='2020-01', lat=30, lon=-90)`.
        The two main objects you'll use are:
    """)
    st.write("- **Dataset** — a collection of variables sharing the same coordinates (like a NetCDF file)")
    st.write("- **DataArray** — a single variable inside a Dataset (e.g. temperature, precipitation)")

    # ── Step 2 ───────────────────────────────────────────────────────────────
    st.header("2. Open a single NetCDF file")
    st.write("Use `xarray.open_dataset()` to load one `.nc` file:")
    st.code("""
import xarray as xr

ds = xr.open_dataset("path/to/your_file.nc")
print(ds)
    """, language="python")
    st.write("`ds` is a Dataset. Printing it shows you all the variables, dimensions, and coordinates inside.")
    st.write("To pull out a single variable as a DataArray:")
    st.code("""
temp = ds["temperature"]
print(temp)
    """, language="python")
    st.info("Tip: use `ds.data_vars` to see all variable names, and `ds.dims` to see dimensions like time, lat, lon.")

    # ── Step 3 ───────────────────────────────────────────────────────────────
    st.header("3. Open multiple files as one dataset")
    st.write("""
        When your data is split across many files (e.g. one file per year),
        use `xarray.open_mfdataset()` to load them all at once.
        It combines them along a dimension — usually `time`.
    """)
    st.code("""
import xarray as xr

ds = xr.open_mfdataset("path/to/data/*.nc", combine="by_coords")
print(ds)
    """, language="python")
    st.write("The `*.nc` wildcard matches all NetCDF files in that folder. xarray stacks them into a single Dataset automatically.")
    st.info("Tip: `open_mfdataset` uses lazy loading — it reads the data only when you actually need it, which keeps memory usage low for large datasets.")
    st.warning("If your files don't combine cleanly, try adding `concat_dim='time'` and `combine='nested'` as arguments.")

    # ── Step 4 ───────────────────────────────────────────────────────────────
    st.header("4. Real example: SPEAR data on the GFDL server")
    st.write("""
        Here's how to open a real dataset you have access to on the GFDL server —
        surface temperature from the SPEAR MED ensemble, SSP5-8.5 scenario.
    """)
    st.write("**Single file:**")
    st.code("""
import xarray as xr

ds = xr.open_dataset(
    "/decp/SPEAR_MED/SPEAR_c192_o1_Scen_SSP585_IC2011_K50/"
    "pp_ens_25/atmos_daily/ts/daily/10yr/"
    "atmos_daily.20150101-20201231.t_surf.nc"
)
print(ds)
    """, language="python")
    st.write("**All 10-year chunks at once:**")
    st.code("""
import xarray as xr

ds = xr.open_mfdataset(
    "/decp/SPEAR_MED/SPEAR_c192_o1_Scen_SSP585_IC2011_K50/"
    "pp_ens_25/atmos_daily/ts/daily/10yr/"
    "atmos_daily.*.t_surf.nc",
    combine="by_coords"
)
print(ds)
    """, language="python")
    st.info("The `*` wildcard matches all date ranges, so xarray stitches the full time series together in one Dataset.")
    # TODO: Add Step 5 — same data accessed from the public SPEAR S3 bucket (cloud access)

    # ── Try it yourself ───────────────────────────────────────────────────────
    st.header("5. Try it yourself")
    st.write("SSH into your GFDL workstation and run the following in a terminal or Jupyter session.")
    st.write("**First, make sure the required packages are installed:**")
    st.code("pip install xarray netcdf4 scipy", language="bash")
    st.write("**Then copy and run these cells:**")
    st.code("""
import xarray as xr

# Single file
ds = xr.open_dataset(
    "/decp/SPEAR_MED/SPEAR_c192_o1_Scen_SSP585_IC2011_K50/"
    "pp_ens_25/atmos_daily/ts/daily/10yr/"
    "atmos_daily.20150101-20201231.t_surf.nc"
)
print(ds)
    """, language="python")
    st.code("""
import xarray as xr

# All 10-year chunks
ds_all = xr.open_mfdataset(
    "/decp/SPEAR_MED/SPEAR_c192_o1_Scen_SSP585_IC2011_K50/"
    "pp_ens_25/atmos_daily/ts/daily/10yr/"
    "atmos_daily.*.t_surf.nc",
    combine="by_coords"
)
print(ds_all)
    """, language="python")
    st.info("GFDL users: make sure you're SSHed into your workstation before running these.")

    # ── Reflect ──────────────────────────────────────────────────────────────
    st.markdown("### Reflect")
    st.info("This is just for you — your responses are not saved.")

    understood = st.radio(
        "Did the difference between `open_dataset` and `open_mfdataset` make sense?",
        ["Yes", "Somewhat", "Not yet"],
        index=None,
    )
    completed = st.checkbox("I ran the code and successfully opened a NetCDF file")

    if understood and completed:
        if understood == "Not yet":
            st.markdown("Take another look at steps 2 and 3 — try running the code with a sample file before moving on.")
        else:
            st.components.v1.html(DONE_HTML, height=60)
    elif understood or completed:
        st.markdown("Take a moment to try the code above before continuing.")
