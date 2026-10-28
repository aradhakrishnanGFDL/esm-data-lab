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
<div class="msg">You know your data formats!</div>
"""


def _grid(hits):
    """A 5 x 4 grid of chunks; the chunks in `hits` are highlighted."""
    cells = "".join(
        f'<div class="hit"></div>' if i in hits else "<div></div>" for i in range(20)
    )
    return f'<div class="grid">{cells}</div>'


VISUAL_HTML = f"""
<style>
  body {{ margin: 0; font-family: sans-serif; background: transparent; }}
  .row {{ display: flex; gap: 12px; }}
  .card {{ flex: 1; background: #f5f7fa; color: #222; border-radius: 10px; padding: 12px; text-align: center; }}
  .card h4 {{ margin: 0 0 8px 0; }}
  .file {{ height: 90px; background: #90a4ae; border-radius: 6px; display: flex;
          align-items: center; justify-content: center; color: #fff; font-weight: 700; }}
  .grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 3px; height: 90px; }}
  .grid div {{ background: #b0bec5; border-radius: 3px; }}
  .grid .hit {{ background: #2e7d32; }}
  .snaps {{ margin-top: 6px; font-size: 12px; }}
  .snaps span {{ background: #1565c0; color: #fff; border-radius: 10px; padding: 2px 8px; margin: 0 2px; }}
  .cap {{ font-size: 13px; margin-top: 8px; }}
</style>
<div class="row">
  <div class="card">
    <h4>NetCDF</h4>
    <div class="file">one file</div>
    <div class="cap">Designed for files on disk. Common for model output.</div>
  </div>
  <div class="card">
    <h4>Zarr</h4>
    {_grid({7, 8})}
    <div class="cap">Many small chunks. Read only the <b style="color:#2e7d32">green</b> ones you need.</div>
  </div>
  <div class="card">
    <h4>Icechunk</h4>
    {_grid({7, 8})}
    <div class="snaps"><span>v1</span>→<span>v2</span>→<span>v3</span></div>
    <div class="cap">Zarr plus safe updates and version history.</div>
  </div>
</div>
"""

QUIZ = [
    (
        "What does chunking let you do?",
        ["Read only the pieces you need", "Make files smaller on disk", "Rename variables automatically"],
        "Read only the pieces you need",
        "Zarr saves arrays in small chunks, so you only fetch the chunks you ask for.",
    ),
    (
        "Which format adds version history (snapshots, branches, tags)?",
        ["NetCDF", "Zarr", "Icechunk"],
        "Icechunk",
        "Icechunk is built on Zarr and adds safe updates and version history.",
    ),
    (
        "You want to rerun your analysis next year on exactly the same data. What helps most?",
        ["Download a fresh copy each time", "Note the Icechunk snapshot or tag you used", "Rerun it with a Zarr store"],
        "Note the Icechunk snapshot or tag you used",
        "Icechunk keeps a version history, so you can open exactly the version you used before.",
    ),
]


def run():
    st.title("Intro to Data Formats: NetCDF, Zarr, Icechunk")
    st.write("""
        Earth system model output comes in different formats, and the format decides how easily you can read it
        from the cloud, share it, and reproduce your results. By the end of this module you'll be able to say
        what each format is for, and you'll have tried all three yourself.
    """)

    st.markdown("**How to use this module:** look at the picture and table, run the four cells in the exercise, then take the quiz.")

    # ══ The three formats ════════════════════════════════════════════════════
    st.header("The three formats at a glance")
    st.components.v1.html(VISUAL_HTML, height=230)
    st.markdown("""
| | NetCDF | Zarr | Icechunk |
|---|---|---|---|
| **Cloud-optimized** | No (a legacy format) | Yes | Yes |
| **Read just a few chunks** | — | Yes | Yes |
| **Version history** | No | No | Yes |
| **Use it when** | Your data is already in NetCDF files | You want to read pieces of large data from the cloud | Data changes, is shared, or must be reproducible |
    """)
    st.info("Icechunk is not a replacement for Zarr. It is built on Zarr and adds safe updates (ACID transactions) and version history (snapshots, branches, tags).")

    # ══ Hands-on ═════════════════════════════════════════════════════════════
    st.header("Hands-on")
    st.write("""
        Run these cells in order in a Jupyter session or Python terminal. Everything runs locally on a small
        example dataset, so no login or cloud access is needed.
    """)
    # TODO: link to the environment module once it exists
    st.code("pip install xarray zarr dask netcdf4 pooch icechunk", language="bash")
    st.caption("New to Python environments? See the environment module for more info.")

    st.subheader(":blue[1. Open a NetCDF file]")
    st.code("""
import xarray as xr

ds = xr.tutorial.open_dataset("rasm")   # a small NetCDF file, downloaded for you
print(ds)
print(list(ds.data_vars))
    """, language="python")
    st.write("Look at the dimensions and the data variables. This is the format you already know.")

    st.subheader(":blue[2. Save it as Zarr]")
    st.code("""
ds.chunk({"time": 1}).to_zarr("rasm.zarr", mode="w")   # one chunk per time step

ds_zarr = xr.open_zarr("rasm.zarr")
var = list(ds_zarr.data_vars)[0]
print(ds_zarr[var].chunks)

one_step = ds_zarr[var].isel(time=0).load()   # reads just one chunk
print(one_step.shape)
    """, language="python")
    st.write("The data is now saved as many small chunks. Reading one time step only reads one chunk.")

    st.subheader(":blue[3. Save it as Icechunk, in two versions]")
    st.code("""
import tempfile
import icechunk as ic
from icechunk.xarray import to_icechunk

repo = ic.Repository.create(ic.local_filesystem_storage(tempfile.mkdtemp()))

n = ds.sizes["time"] // 2
part1 = ds.isel(time=slice(None, n))
part2 = ds.isel(time=slice(n, None))

# Version 1: the first half of the data
session = repo.writable_session("main")
to_icechunk(part1, session)
snap1 = session.commit("first half of the data")

# Version 2: add the rest
session = repo.writable_session("main")
to_icechunk(part2, session, append_dim="time")
snap2 = session.commit("add the second half")
    """, language="python")
    st.write("Each `commit` saves a snapshot. Nothing was overwritten: version 1 is still there.")

    st.subheader(":blue[4. Go back in time]")
    st.code("""
latest = xr.open_zarr(repo.readonly_session("main").store, consolidated=False)
v1 = xr.open_zarr(repo.readonly_session(snapshot_id=snap1).store, consolidated=False)

print("latest:   ", latest.sizes["time"], "time steps")
print("version 1:", v1.sizes["time"], "time steps")
    """, language="python")
    st.write("You should see more time steps in the latest version than in version 1. That is version history.")

    completed = st.checkbox("I ran the four cells and saw both versions")

    # ══ Quiz ═════════════════════════════════════════════════════════════════
    st.header("Quiz")
    st.info("This is just for you — your responses are not saved.")

    correct = 0
    for i, (question, options, answer, why) in enumerate(QUIZ):
        choice = st.radio(question, options, index=None, key=f"formats_quiz_{i}")
        if choice is not None:
            if choice == answer:
                st.success(f"Correct. {why}")
                correct += 1
            else:
                st.error("Not quite. Try again.")

    if completed and correct == len(QUIZ):
        st.components.v1.html(DONE_HTML, height=60)
    elif correct == len(QUIZ):
        st.markdown("Nice work on the quiz. Run the hands-on cells too, then tick the box above.")
    elif completed:
        st.markdown("Good, you ran the cells. Finish the quiz to wrap up.")

    # ══ Next ═════════════════════════════════════════════════════════════════
    st.info("""
        **Did you know?** You don't have to rewrite your NetCDF files to use Zarr or Icechunk.
        A tool called VirtualiZarr can create a "virtual" dataset that points to the data inside
        your existing files, without copying them. Curious? Ask us about VirtualiZarr
        and we'll add a module on it.
    """)
    # TODO: link to the next module
    st.write("**Next:** *Finding Cloud Data: Catalogs and Arraylake*, where you learn how to find datasets in the cloud.")

    with st.expander("Dig deeper: references"):
        st.markdown("""
- [Zarr](https://zarr.dev/) — the array format
- [Why Icechunk?](https://icechunk.io/en/stable/overview/) — what Icechunk adds to Zarr
- [Icechunk core concepts](https://icechunk.io/en/stable/understanding/concepts/) — transactions, snapshots, branches, tags
- [Icechunk + Xarray](https://icechunk.io/en/stable/guides/xarray/) — the writing and reading pattern used above
- [VirtualiZarr](https://virtualizarr.readthedocs.io/)
        """)
