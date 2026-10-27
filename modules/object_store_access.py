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
<div class="msg">☁️ You're pulling data from the cloud like a pro!</div>
"""


def run():
    st.title("Cloud Data Access with Arraylake")
    st.write("""
        Arraylake lets you read large earth system model datasets straight from the cloud — no files to
        copy, no server path to remember. By the end of this module you'll be able to connect
        to the SPEAR large ensemble through Arraylake, open it with xarray, and pull a field into memory.
        We also compare this with other ways of accessing the same kind of data.
    """)
    # TODO: link to the environment module once it exists
    st.info("Make sure the packages are installed: `pip install arraylake xarray zarr`. New to Python environments? See the environment module for more info.")

    # ══ Main section: Why Arraylake? ═════════════════════════════════════════
    st.header("Why Arraylake?")
    st.write("""
        **The problem.** Earth system model output is too big to keep downloading and copying around.
        Instead, we want to bring the analysis to the data. That means:
    """)
    st.write("- **No download** (lazy loading, streaming) — read only the piece you need")
    st.write("- **Analysis comes to the data** (cloud-native) — your code works on the data where it lives, in the cloud")
    st.write("- **Fast** (chunking, parallel reads) — reading a small piece shouldn't mean loading everything")
    st.write("- **Versioned** (snapshots, tags) — know exactly which version of the data you used, so results can be reproduced")
    st.write("""
        **The solution.** Cloud-optimized formats like Zarr save big arrays in small pieces called
        chunks (chunking), so you only fetch the chunks you ask for, and the data can live in cloud storage.
    """)
    st.write("""
        **Icechunk: our first example.** Icechunk is a free, open-source tool built on Zarr. It adds
        safe updates (ACID transactions) and a version history (snapshots, branches, tags), so you
        can go back to the data as it was earlier. We start with Icechunk, but it isn't the only way
        to access data, and we compare other ways in this module.
    """)
    st.write("""
        **Arraylake: the way in.** Arraylake is Earthmover's managed platform built on Icechunk.
        It gives you a catalog for finding datasets and a way to share them, and you read them from
        Python with your Arraylake login.
    """)
    st.write("""
        The cloud storage where the data sits is called an **object store**.
        New to object stores? See the intro to object stores module (coming soon).
    """)
    # TODO: link to the object store intro module once it exists
    st.caption(
        "Learn more: [Arraylake documentation](https://docs.earthmover.io/) · "
        "[Icechunk: Arraylake](https://icechunk.io/en/stable/arraylake/) · "
        "[Why Icechunk?](https://icechunk.io/en/stable/overview/)"
    )

    # ══ Hands-on: same steps, two ways ═══════════════════════════════════════
    st.header("Hands-on")
    st.write("""
        Start with the Arraylake (Icechunk) tab: connect, find the data, open it, and pull a field.
        The second tab will repeat the same steps with other ways of accessing data, for comparison.
    """)

    tab_arraylake, tab_zarr = st.tabs(["Arraylake (Icechunk)", "Zarr & other catalogs"])

    # ── Tab A: Arraylake / Icechunk ──────────────────────────────────────────
    with tab_arraylake:
        st.caption("Reading the SPEAR ensemble through Arraylake: a login, a catalog, and version history.")

        st.subheader("1. Connect to the repository")
        st.write("Set your token as an environment variable before starting Python or Jupyter:")
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
        st.write("`session.store` is what xarray and zarr use to read from the cloud. Nothing has been downloaded yet.")
        st.write("Because you read from a branch, everyone reading `main` sees the same version of the data.")

        st.subheader("2. Find the data")
        st.write("The data is organized as `<experiment>/<table>`. Use zarr to see what's there:")
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

        st.subheader("3. Open a group with xarray")
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
        st.write("There are 30 ensemble members (`member_id`) and 1128 monthly time steps in this group.")

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
        st.write("Because the data is chunked by month and member, this fetches a single map instead of the whole archive.")

        st.subheader("5. Try it yourself")
        st.write("Run this in a terminal or Jupyter session with `ARRAYLAKE_TOKEN` set:")
        st.code("""
import warnings
warnings.filterwarnings("ignore")  # zarr codec-config warnings are noise here

from arraylake import Client
import numpy as np
import xarray as xr

client = Client()                                  # auth from ARRAYLAKE_TOKEN
repo = client.get_repo("GFDL/noaa-gfdl-spear-large-ensembles-pds")
session = repo.readonly_session(branch="main")

ds = xr.open_zarr(session.store, group="historical/Amon", consolidated=False)

da = ds["tas"].sel(member_id="r1i1p1f1", time="2000-07").isel(time=0).load()
print(da.shape, "global mean:", float(np.nanmean(da.values)), da.attrs["units"])
        """, language="python")
        st.info("If you get an authentication error, check that `ARRAYLAKE_TOKEN` is set in the same terminal or kernel you're running from.")

    # ── Tab B: Zarr & other catalogs ─────────────────────────────────────────
    with tab_zarr:
        st.info("TODO: NetCDF and Zarr access are coming soon.")
        # TODO: same five steps as the Arraylake tab (connect, find the data, open, pull a field, try it yourself)
        # TODO: NetCDF access (public bucket location, open_dataset / open_mfdataset)
        # TODO: Zarr access (public bucket location, open_zarr)
        # TODO: decide which other catalog(s) to compare
        # TODO: add a short "What's different from Arraylake?" comparison

    # ══ Dig deeper ═══════════════════════════════════════════════════════════
    st.info("""
        **Did you know?** You don't have to rewrite your NetCDF files to use Icechunk and Zarr.
        A tool called VirtualiZarr can create a "virtual" dataset that points to the data inside
        your existing files, without copying or modifying them. Curious? Ask us about VirtualiZarr
        and we'll add a module on it.
    """)

    with st.expander("Dig deeper: references"):
        st.markdown("""
**Concepts**
- [Zarr](https://zarr.dev/) — the array format (chunking)
- [Why Icechunk?](https://icechunk.io/en/stable/overview/) — ACID transactions and version history
- [Icechunk core concepts](https://icechunk.io/en/stable/understanding/concepts/) — transactions, snapshots, branches, tags, chunks
- [Icechunk FAQ](https://icechunk.io/en/latest/faq/)

**Arraylake**
- [Arraylake documentation](https://docs.earthmover.io/)
- [Icechunk and Arraylake](https://icechunk.io/en/stable/arraylake/)
- [Authentication and API tokens](https://docs.earthmover.io/setup/org-access)

**Reading the data**
- [xarray.open_zarr](https://docs.xarray.dev/en/latest/generated/xarray.open_zarr.html) — opening a Zarr store (lazy loading)

**The dataset**
- [GFDL SPEAR Large Ensembles](https://www.gfdl.noaa.gov/?p=79810)
- [Delworth et al. (2020), SPEAR model description](https://doi.org/10.1029/2019MS001895)

**Working with existing NetCDF files**
- [VirtualiZarr](https://virtualizarr.readthedocs.io/)
- [Icechunk virtual datasets](https://icechunk.io/en/stable/guides/virtual/)
        """)

    # ── Reflect ──────────────────────────────────────────────────────────────
    st.markdown("### Reflect")
    st.info("This is just for you — your responses are not saved.")

    understood = st.radio(
        "Did the idea of lazy loading (nothing downloads until `.load()`) make sense?",
        ["Yes", "Somewhat", "Not yet"],
        index=None,
    )
    completed = st.checkbox("I ran the code and successfully loaded a field from the Arraylake repo")

    if understood and completed:
        if understood == "Not yet":
            st.markdown("Take another look at steps 3 and 4 in the Hands-on section — try printing `ds['tas']` before and after calling `.load()` to see the difference.")
        else:
            st.components.v1.html(DONE_HTML, height=60)
    elif understood or completed:
        st.markdown("Take a moment to try the code above before continuing.")
