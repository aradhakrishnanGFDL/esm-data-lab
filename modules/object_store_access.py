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
<div class="msg">☁️ You know where to look and how to start!</div>
"""


def run():
    st.title("Finding Earth System Data: Catalogs and Arraylake")
    # TODO: link to the intro to data formats module once it exists
    st.write("""
        In the previous module, *Intro to Data Formats*, you learned how NetCDF, Zarr and Icechunk store data
        and how to open them when you already know where the data is. This module is about the step before that:
        **finding** the data. You'll learn which catalog to use for which kind of data, and how to get started quickly.
    """)

    # ══ Why catalogs? ════════════════════════════════════════════════════════
    st.header("Why catalogs?")
    st.write("""
        Cloud datasets are huge and there are many of them. Before you can read anything, you need to know:
        What datasets exist? Where is each one stored? How do I open it?
        A **catalog** is a searchable list of datasets and where to find them. You search it, and it gives you what
        you need to open the data.
    """)
    # TODO: link to the catalogs module once it exists
    st.info("**Coming soon:** a separate module covers catalog specifications and how catalogs are created. Here, we focus on using them.")

    # ══ What should I use? ═══════════════════════════════════════════════════
    st.header("Which one should I use?")
    st.markdown("""
| If you want to... | Use |
|---|---|
| Search CMIP6-style model output that is already in the cloud (NetCDF or Zarr) | **intake-esm** |
| Find CMIP7 STAC-indexed data through ESGF| **intake-esgf** (examples coming soon) |
| Read data in an Arraylake repository, such as SPEAR, or share your own data with your team | **Arraylake** |
| Search spatiotemporal data in general from satellite imagery to earth system data with a web browser | **STAC** (coming soon) |
    """)

    st.subheader("Install what you need")
    # TODO: link to the environment module once it exists
    st.code("""
pip install intake-esm xarray zarr s3fs h5netcdf   # intake-esm
pip install arraylake xarray zarr                  # Arraylake
pip install icechunk                               # only for opening Icechunk repos without Arraylake
pip install intake-esgf                            # intake-esgf
    """, language="bash")
    st.caption("New to Python environments? See the environment module for more info.")

    # ══ Hands-on ═════════════════════════════════════════════════════════════
    st.header("Quick start")
    st.write("""
        Pick a tab. Each quick start follows the same four steps: :blue[**open the catalog**], :blue[**find the data**],
        :blue[**open the data**], and :blue[**pull a field**].
    """)

    tab_intake, tab_arraylake, tab_esgf, tab_stac = st.tabs(
        ["intake-esm (CMIP6)", "Arraylake (SPEAR)", "intake-esgf (soon)", "STAC (soon)"]
    )

    # ── Tab: intake-esm ──────────────────────────────────────────────────────
    with tab_intake:
        st.write("""
            intake-esm works the same way whatever format the data is in. Here it searches CMIP6 model output
            stored as NetCDF files in a public bucket. No login needed.
        """)
        st.code("""
import intake

# 1. Open the catalog
col = intake.open_esm_datastore(
    "https://raw.githubusercontent.com/aradhakrishnanGFDL/gfdl-aws-analysis/master/esm-collection-spec-examples/esgf-world.json"
)

# 2. Find the data: monthly ocean sea surface temperature from GFDL-ESM4
cat = col.search(
    source_id=["GFDL-ESM4"], experiment_id=["historical"], table_id=["Omon"],
    member_id=["r1i1p1f1"], grid_label=["gn"], variable_id=["tos"],
)
cat = cat.search(version=cat.df.version.max())   # keep only the latest version

# 3. Open the data (lazy: nothing downloads yet)
dset_dict = cat.to_dataset_dict(
    storage_options=dict(anon=True),
    cdf_kwargs={"decode_times": True, "chunks": {"time": 1}},
)
ds = dset_dict[list(dset_dict)[0]]

# 4. Pull a field into memory
da = ds["tos"].isel(time=0).squeeze().load()
print(da.shape, float(da.mean()))
        """, language="python")

        st.write("""
            **Zarr instead of NetCDF?** Only two lines change. Everything else is :green[**the same**].
        """)
        st.code("""
# Zarr: use Pangeo's CMIP6 catalog, and zarr_kwargs instead of cdf_kwargs
col = intake.open_esm_datastore("https://cmip6-pds.s3.amazonaws.com/pangeo-cmip6.json")

dset_dict = cat.to_dataset_dict(
    storage_options=dict(anon=True),
    zarr_kwargs={"consolidated": True},
)
        """, language="python")
        st.write(":orange[**Different:**] the catalog URL, and `zarr_kwargs` replaces `cdf_kwargs`. The search, the dataset, and the field you pull are :green[**the same**].")

        # TODO: link to the full walkthrough notebook
        st.caption("Want the full walkthrough? Open the notebook (coming soon).")

        with st.expander("Step-by-step walkthrough"):
            tab_nc, tab_zarr = st.tabs(["NetCDF files", "Zarr stores"])

            # ── NetCDF ───────────────────────────────────────────────────────
            with tab_nc:
                st.caption("Searching CMIP6 model output stored as NetCDF files in a public bucket.")

                st.subheader(":blue[1. Open the catalog]")
                st.code("""
import intake

col_url = "https://raw.githubusercontent.com/aradhakrishnanGFDL/gfdl-aws-analysis/master/esm-collection-spec-examples/esgf-world.json"
col = intake.open_esm_datastore(col_url)
                """, language="python")
                st.write("Opening the catalog reads a table describing the available datasets, not the data itself.")

                st.subheader(":blue[2. Find the data]")
                st.write("Describe what you want, and search. Here: monthly ocean sea surface temperature (`tos`) from GFDL-ESM4.")
                st.code("""
query = dict(
    source_id=["GFDL-ESM4"],
    experiment_id=["historical"],
    table_id=["Omon"],
    member_id=["r1i1p1f1"],
    grid_label=["gn"],
    variable_id=["tos"],
)

cat = col.search(**query)
cat = cat.search(version=cat.df.version.max())   # keep only the latest version
print(len(cat.df), "files found")
                """, language="python")

                st.subheader(":blue[3. Open the data]")
                st.code("""
dset_dict = cat.to_dataset_dict(
    storage_options=dict(anon=True),
    cdf_kwargs={"decode_times": True, "chunks": {"time": 1}},
)
print(list(dset_dict))

key = list(dset_dict)[0]     # the dataset's name; only one dataset matches our query
ds = dset_dict[key]
                """, language="python")
                st.write("""
                    intake-esm returns a dictionary of xarray datasets. Each name is built from the project,
                    institution, model, experiment and table, for example `CMIP6.NOAA-GFDL.GFDL-ESM4.historical.Omon`.
                    `cdf_kwargs` are the options for opening NetCDF files.
                """)
                st.info("The datasets are lazy: data only downloads when you call `.load()`, `.values`, or plot.")

                st.subheader(":blue[4. Pull a field into memory]")
                st.code("""
da = ds["tos"].isel(time=0).squeeze().load()

print(da.shape, da.attrs.get("units"))
print("global mean:", float(da.mean()))
                """, language="python")
                st.write("`.squeeze()` drops dimensions of length 1, such as the single ensemble member we asked for.")
                st.info(""".squeeze()` removes dimensions of length 1. It changes the shape, not the data.

    - before: `(member_id: 1, y: 576, x: 720)`
    - after: `(y: 576, x: 720)`
""")

            # ── Zarr ─────────────────────────────────────────────────────────
            with tab_zarr:
                st.caption("""
                    The same four steps with CMIP6 data stored as Zarr stores (Pangeo's CMIP6 catalog on AWS).
                    Look for the :green[**Same**] and :orange[**Different**] notes: they mark what changes from the NetCDF version.
                """)

                st.subheader(":blue[1. Open the catalog]")
                st.code("""
import intake

col_url = "https://cmip6-pds.s3.amazonaws.com/pangeo-cmip6.json"
col = intake.open_esm_datastore(col_url)
                """, language="python")
                st.write(":orange[**Different:**] a different catalog URL. This catalog lists Zarr stores instead of NetCDF files.")

                st.subheader(":blue[2. Find the data]")
                st.code("""
query = dict(
    source_id=["GFDL-ESM4"],
    experiment_id=["historical"],
    table_id=["Omon"],
    member_id=["r1i1p1f1"],
    grid_label=["gn"],
    variable_id=["tos"],
)

cat = col.search(**query)
cat = cat.search(version=cat.df.version.max())   # keep only the latest version
print(len(cat.df), "stores found")
                """, language="python")
                st.write(":green[**Same:**] the same query and the same search. Both catalogs use the same CMIP6 column names. Each row is now a Zarr store instead of a NetCDF file.")

                st.subheader(":blue[3. Open the data]")
                st.code("""
dset_dict = cat.to_dataset_dict(
    storage_options=dict(anon=True),
    zarr_kwargs={"consolidated": True},
)
print(list(dset_dict))

key = list(dset_dict)[0]     # the dataset's name; only one dataset matches our query
ds = dset_dict[key]
                """, language="python")
                st.write(":orange[**Different:**] `zarr_kwargs` replaces `cdf_kwargs`. The option `consolidated=True` reads the store's metadata in one go, as it did with `xr.open_zarr`.")
                st.write("""
                    :orange[**Different:**] dataset names follow the same pattern with the grid label added at the end,
                    for example `ScenarioMIP.THU.CIESM.ssp585.Amon.gr` in the Pangeo docs.
                """)
                st.info("Still lazy: data only downloads when you call `.load()`, `.values`, or plot.")

                st.subheader(":blue[4. Pull a field into memory]")
                st.code("""
da = ds["tos"].isel(time=0).squeeze().load()

print(da.shape, da.attrs.get("units"))
print("global mean:", float(da.mean()))
                """, language="python")
                st.write(":green[**Same:**] exactly the same code as the NetCDF version. Once the dataset is open, xarray doesn't care what format it came from.")

    # ── Tab: Arraylake ───────────────────────────────────────────────────────
    with tab_arraylake:
        st.write("""
            Arraylake is Earthmover's managed platform, built on Icechunk. It gives you a catalog for finding datasets
            and a way to share them. Here it serves the SPEAR large ensemble. A login is required: set your token first with
            `export ARRAYLAKE_TOKEN="your-token-here"`.
        """)
        st.code("""
from arraylake import Client
import xarray as xr

# 1. Open the repository
client = Client()                       # auth from ARRAYLAKE_TOKEN
repo = client.get_repo("GFDL/noaa-gfdl-spear-large-ensembles-pds")
session = repo.readonly_session(branch="main")

# 2. Find the data: browse the groups in the repository
#    (see the walkthrough below)

# 3. Open the data (lazy: nothing downloads yet)
ds = xr.open_zarr(session.store, group="historical/Amon", consolidated=False)

# 4. Pull a field into memory
da = ds["tas"].sel(member_id="r1i1p1f1", time="2000-07").isel(time=0).load()
print(da.shape, float(da.mean()))
        """, language="python")
        st.warning("Treat your token like a password. Never paste it into a notebook or share it in chat.")

        # TODO: link to the full walkthrough notebook
        st.caption("Want the full walkthrough? Open the notebook (coming soon).")

        with st.expander("Step-by-step walkthrough"):
            st.subheader(":blue[1. Open the repository]")
            st.write("**Option A: through Arraylake.** Connect to the repo and open a read-only session on the `main` branch:")
            st.code("""
from arraylake import Client

ARRAYLAKE_REPO = "GFDL/noaa-gfdl-spear-large-ensembles-pds"
ARRAYLAKE_BRANCH = "main"

client = Client()                       # auth from ARRAYLAKE_TOKEN
repo = client.get_repo(ARRAYLAKE_REPO)
session = repo.readonly_session(branch=ARRAYLAKE_BRANCH)
            """, language="python")
            st.write("""
                **Option B: directly with Icechunk.** Icechunk works on its own. Instead of asking Arraylake
                for the repo by name, you point Icechunk at where the data is stored. This option is useful
                if your Icechunk repos are not hosted in Arraylake.
            """)
            st.code("""
import icechunk

# TODO: bucket and prefix of the Icechunk repo, and how to authenticate
storage = icechunk.s3_storage(bucket="<bucket>", prefix="<prefix>", from_env=True)
repo = icechunk.Repository.open(storage)
session = repo.readonly_session("main")
            """, language="python")
            st.caption("Needs `pip install icechunk`. Learn more: [Icechunk how-to](https://icechunk.io/en/latest/getting-started/howto/)")
            st.write("Either way, you end up with a `session`. `session.store` is what xarray and zarr use to read from the cloud, and nothing has been downloaded yet.")

            st.subheader(":blue[2. Find the data]")
            st.write("Instead of searching, you browse the repository. The data is organized as `<experiment>/<table>`:")
            st.code("""
import zarr

root = zarr.open_group(session.store, mode="r")

for experiment in sorted(root.group_keys()):
    print(experiment, sorted(root[experiment].group_keys()))
            """, language="python")
            st.code("""
historical       ['6hr', 'Amon', 'Ofx', 'Omon', 'day', 'fx']
scenarioSSP5-85  ['6hr', 'Amon', 'Ofx', 'Omon', 'day', 'fx']
            """, language="text")
            st.write("""
                `historical` covers 1921–2014 and `scenarioSSP5-85` covers 2015–2100.
                `Amon` is monthly atmosphere data, which is what we'll use here.
            """)

            st.subheader(":blue[3. Open the data]")
            st.code("""
import xarray as xr

ds = xr.open_zarr(session.store, group="historical/Amon", consolidated=False)
print(list(ds.data_vars))
print(dict(ds.sizes))
            """, language="python")
            st.code("""
['hus', 'pr', 'rlut', 'rsut', 'sfcWind', 'ta', 'tas', 'ua', 'rsdt', 'psl', 'zg', 'uas', 'va', 'vas']
{'member_id': 30, 'time': 1128, 'plev': 17, 'lat': 360, 'lon': 576, ...}
            """, language="text")
            st.info("`consolidated=False` is required for Icechunk stores. The Dataset is lazy: data only downloads when you call `.load()`, `.values`, or plot.")

            st.subheader(":blue[4. Pull a field into memory]")
            st.write("Select with labels, then `.load()` to fetch just that piece — here, one member, one month, the whole globe:")
            st.code("""
import numpy as np

da = ds["tas"].sel(member_id="r1i1p1f1", time="2000-07").isel(time=0).load()

print(da.shape, da.attrs["units"])
print("global mean:", float(np.nanmean(da.values)))
            """, language="python")
            st.code("""
(360, 576) K
global mean: 280.28509521484375
            """, language="text")
            st.info("If you get an authentication error, check that `ARRAYLAKE_TOKEN` is set in the same terminal or kernel you're running from.")

    # ── Tab: intake-esgf (coming soon) ───────────────────────────────────────
    with tab_esgf:
        st.write("""
            **intake-esgf** gives you programmatic access to ESGF holdings. If you know intake-esm, it will feel familiar.
            Instead of opening a catalog file, you search one or more ESGF index nodes. The files are then downloaded
            into a local cache and loaded for you, so your search becomes the way you get the data.
        """)
        st.code("pip install intake-esgf", language="bash")
        st.info("**Examples coming soon.**")
        # TODO: add intake-esgf examples

    # ── Tab: STAC (coming soon) ──────────────────────────────────────────────
    with tab_stac:
        st.write("""
            **STAC** (SpatioTemporal Asset Catalog) is another way to describe and search datasets. It is used for
            satellite imagery and other geospatial data.
        """)
        st.info("**Did you know?** STAC catalogs can be searched much like the catalogs above. **Examples coming soon.**")
        # TODO: add STAC examples

    # ══ Try it yourself ══════════════════════════════════════════════════════
    st.header("Try it yourself")
    st.write("""
        The quick starts above are ready to copy and run in a terminal or Jupyter session. For the Arraylake tab,
        set `ARRAYLAKE_TOKEN` first. For a guided walkthrough, open the notebook (coming soon).
    """)
    # TODO: link to the notebook

    # ══ Dig deeper ═══════════════════════════════════════════════════════════
    st.info("""
        **Did you know?** You can combine catalogs with VirtualiZarr and Icechunk, so you don't have to convert your
        NetCDF files. For example, the intake-virtual-icechunk package builds a virtual Icechunk store from an
        intake-esm catalog. Details coming soon.
    """)

    with st.expander("Dig deeper: references"):
        st.markdown("""
**Catalogs and CMIP6**
- [Pangeo: accessing CMIP6 in the cloud](https://pangeo-data.github.io/pangeo-cmip6-cloud/accessing_data.html) — intake-esm and Zarr examples
- [CMIP6 on AWS (Registry of Open Data)](https://registry.opendata.aws/cmip6)
- [The esgf-world catalog (NetCDF) used above](https://raw.githubusercontent.com/aradhakrishnanGFDL/gfdl-aws-analysis/master/esm-collection-spec-examples/esgf-world.json)
- [The Pangeo CMIP6 catalog (Zarr) used above](https://cmip6-pds.s3.amazonaws.com/pangeo-cmip6.json)
- [intake-esgf documentation](https://intake-esgf.readthedocs.io/)
- [intake-virtual-icechunk](https://intake-virtual-icechunk.readthedocs.io)

**Arraylake**
- [Arraylake documentation](https://docs.earthmover.io/)
- [Icechunk and Arraylake](https://icechunk.io/en/stable/arraylake/)
- [Authentication and API tokens](https://docs.earthmover.io/setup/org-access)
- [Why Icechunk?](https://icechunk.io/en/stable/overview/)

**Reading the data**
- [xarray.open_zarr](https://docs.xarray.dev/en/latest/generated/xarray.open_zarr.html) — opening a Zarr store (lazy loading)

**The SPEAR dataset**
- [GFDL SPEAR Large Ensembles](https://www.gfdl.noaa.gov/?p=79810)
- [Delworth et al. (2020), SPEAR model description](https://doi.org/10.1029/2019MS001895)
        """)

    # ── Reflect ──────────────────────────────────────────────────────────────
    st.markdown("### Reflect")
    st.info("This is just for you — your responses are not saved.")

    understood = st.radio(
        "After reading the table above, could you pick the right catalog for your own data?",
        ["Yes", "Somewhat", "Not yet"],
        index=None,
    )
    completed = st.checkbox("I ran at least one quick start and loaded a field")

    if understood and completed:
        if understood == "Not yet":
            st.markdown("Take another look at the *Which one should I use?* table, then try the quick start for the catalog closest to your data.")
        else:
            st.components.v1.html(DONE_HTML, height=60)
    elif understood or completed:
        st.markdown("Take a moment to try the code above before continuing.")
