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
        Arraylake lets you read large climate datasets straight from the cloud — no files to
        copy, no server path to remember. By the end of this module you'll be able to connect
        to the SPEAR large ensemble, open it with xarray, and pull a field into memory.
    """)
    st.info("Make sure the packages are installed: `pip install arraylake xarray zarr`")

    # ── Step 1 ───────────────────────────────────────────────────────────────
    st.header("1. What is Arraylake?")
    st.write("""
        Arraylake stores data in cloud object storage as a versioned **repository**,
        a bit like a Git repo for arrays. Four pieces to keep straight:
    """)
    st.write("- **Client** — your authenticated connection")
    st.write("- **Repo** — a named collection of datasets")
    st.write("- **Branch** — a version of the repo (like `main`)")
    st.write("- **Session** — a read-only view of one branch")

    # ── Step 2 ───────────────────────────────────────────────────────────────
    st.header("2. Connect to the repository")
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

    # ── Step 3 ───────────────────────────────────────────────────────────────
    st.header("3. Find the data")
    st.write("""
        The data is organized as `<experiment>/<table>`. Use zarr to see what's there:
    """)
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

    # ── Step 4 ───────────────────────────────────────────────────────────────
    st.header("4. Open a group with xarray")
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

    # ── Step 5 ───────────────────────────────────────────────────────────────
    st.header("5. Pull a field into memory")
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
    st.info("Tip: longitudes in this dataset run 0–360, not -180–180, so use `lon % 360` when selecting a western-hemisphere point.")

    # ── Try it yourself ───────────────────────────────────────────────────────
    st.header("6. Try it yourself")
    st.write("Run this in a terminal or Jupyter session with `ARRAYLAKE_TOKEN` set:")
    st.code("pip install arraylake xarray zarr", language="bash")
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
            st.markdown("Take another look at steps 4 and 5 — try printing `ds['tas']` before and after calling `.load()` to see the difference.")
        else:
            st.components.v1.html(DONE_HTML, height=60)
    elif understood or completed:
        st.markdown("Take a moment to try the code above before continuing.")
