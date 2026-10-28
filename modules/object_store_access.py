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
<div class="msg">☁️ You're finding and pulling cloud data like a pro!</div>
"""


def run():
    st.title("Finding Cloud Data: Catalogs and Arraylake")
    st.write("""
        Reading data from the cloud is easy once you know where it is. The harder part is finding it.
        In this module you'll use two kinds of catalogs: intake-esm, to search CMIP6 model output,
        and Arraylake, to browse the SPEAR large ensemble.
    """)
    # TODO: link to the environment module once it exists
    st.info("Make sure the packages are installed: `pip install intake-esm arraylake xarray zarr s3fs`. New to Python environments? See the environment module for more info.")

    # ══ Main section: Why catalogs? ══════════════════════════════════════════
    st.header("Why catalogs?")
    st.write("""
        **The problem.** Cloud datasets are huge and there are many of them. Before you can read anything,
        you need to know: What datasets exist? Where is each one stored? How do I open it?
    """)
    st.write("""
        **The solution.** A **catalog** is a searchable list of datasets and where to find them.
        You search it, and it gives you what you need to open the data.
    """)
    st.write("- **intake-esm** — a catalog for earth system model output like CMIP6. You search by model, experiment and variable, and get xarray datasets back.")
    st.write("- **Arraylake** — Earthmover's managed platform, built on Icechunk. It gives you a catalog for finding datasets and a way to share them. You log in, browse a repository, and read from the cloud.")
    st.write("""
        The cloud storage where the data sits is called an **object store**.
        New to object stores? See the intro to object stores module (coming soon).
    """)
    # TODO: link to the object store intro module once it exists
    st.caption(
        "Learn more: [Arraylake documentation](https://docs.earthmover.io/) · "
        "[Pangeo: accessing CMIP6 in the cloud](https://pangeo-data.github.io/pangeo-cmip6-cloud/accessing_data.html)"
    )

    # ══ Hands-on ═════════════════════════════════════════════════════════════
    st.header("Hands-on")
    st.write("""
        Pick a tab. The steps are the same in each: open the catalog, find the data, open it, and pull a field.
    """)

    tab_intake, tab_arraylake = st.tabs(["intake-esm (CMIP6)", "Arraylake (SPEAR)"])

    # ── Tab A: intake-esm ────────────────────────────────────────────────────
    with tab_intake:
        st.caption("Searching CMIP6 model output (NetCDF files in a public bucket) with intake-esm. No login needed.")

        st.subheader("1. Open the catalog")
        st.code("""
import intake

col_url = "https://raw.githubusercontent.com/aradhakrishnanGFDL/gfdl-aws-analysis/master/esm-collection-spec-examples/esgf-world.json"
col = intake.open_esm_datastore(col_url)
        """, language="python")
        st.write("Opening the catalog reads a table describing the available datasets, not the data itself.")

        st.subheader("2. Find the data")
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

        st.subheader("3. Open the data")
        st.code("""
dset_dict = cat.to_dataset_dict(
    storage_options=dict(anon=True),
    cdf_kwargs={"decode_times": True, "chunks": {"time": 1}},
)
print(list(dset_dict))

ds = dset_dict["CMIP6.NOAA-GFDL.GFDL-ESM4.historical.Omon"]
        """, language="python")
        st.write("intake-esm returns a dictionary of xarray datasets, named by project, institution, model, experiment and table.")
        st.info("The datasets are lazy: data only downloads when you call `.load()`, `.values`, or plot.")

        st.subheader("4. Pull a field into memory")
        st.code("""
da = ds["tos"].isel(member_id=0, time=0).load()

print(da.shape, da.attrs.get("units"))
print("global mean:", float(da.mean()))
        """, language="python")

        st.info("""
            Same pattern with Zarr: intake-esm also works with catalogs of Zarr data, like Pangeo's
            CMIP6 catalog (`https://cmip6-pds.s3.amazonaws.com/pangeo-cmip6.json`). The search is the same,
            and opening uses `zarr_kwargs={"consolidated": True}` instead of `cdf_kwargs`.
        """)
        # TODO: add a tested Zarr cell for intake-esm

    # ── Tab B: Arraylake ─────────────────────────────────────────────────────
    with tab_arraylake:
        st.caption("Browsing the SPEAR large ensemble in an Arraylake repository. A login is required.")

        st.subheader("1. Open the repository")
        st.write("**Option A: through Arraylake.** Set your token as an environment variable before starting Python or Jupyter:")
        st.code('export ARRAYLAKE_TOKEN="your-token-here"', language="bash")
        st.warning("Treat your token like a password. Never paste it into a notebook or share it in chat.")
        st.write("Then connect to the repo and open a read-only session on the `main` branch:")
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

        st.subheader("2. Find the data")
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

        st.subheader("3. Open the data")
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

        st.subheader("4. Pull a field into memory")
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

    # ══ Try it yourself ══════════════════════════════════════════════════════
    st.header("Try it yourself")
    st.write("""
        Run the code blocks from one tab in order in a terminal or Jupyter session. They build on each other.
        For the Arraylake tab, set `ARRAYLAKE_TOKEN` first.
    """)

    # ══ Dig deeper ═══════════════════════════════════════════════════════════
    st.info("""
        **Did you know?** intake-esm and Arraylake are not the only catalogs. Others, such as STAC,
        are used across the earth sciences. Curious? Ask us about STAC and we'll add a module on it.
    """)

    with st.expander("Dig deeper: references"):
        st.markdown("""
**Catalogs and CMIP6**
- [Pangeo: accessing CMIP6 in the cloud](https://pangeo-data.github.io/pangeo-cmip6-cloud/accessing_data.html) — intake-esm and Zarr examples
- [CMIP6 on AWS (Registry of Open Data)](https://registry.opendata.aws/cmip6)
- [The esgf-world catalog used above](https://raw.githubusercontent.com/aradhakrishnanGFDL/gfdl-aws-analysis/master/esm-collection-spec-examples/esgf-world.json)

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
        "Did the difference between searching a catalog (intake-esm) and browsing a repository (Arraylake) make sense?",
        ["Yes", "Somewhat", "Not yet"],
        index=None,
    )
    completed = st.checkbox("I ran the code from at least one tab and loaded a field")

    if understood and completed:
        if understood == "Not yet":
            st.markdown("Take another look at steps 2 and 3 in each tab — try printing what the search or the repository browse returns.")
        else:
            st.components.v1.html(DONE_HTML, height=60)
    elif understood or completed:
        st.markdown("Take a moment to try the code above before continuing.")
