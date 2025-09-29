# Load packages into current runtime
import datetime as dt
import getpass
import os

import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from xarray.plot.utils import label_from_attrs

from harmony import BBox, Client, Collection, Request
from harmony.config import Environment
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

client_id = os.getenv("TEMPO_CLIENT_ID")
client_secret = os.getenv("TEMPO_CLIENT_SECRET")
harmony_client = Client(auth=(client_id, client_secret))

data_proj = ccrs.PlateCarree()


def make_nice_map(axis):
    axis.add_feature(cfeature.STATES, color="gray", lw=0.1)
    axis.coastlines(resolution="50m", color="gray", linewidth=0.5)

    axis.set_extent([-150, -40, 14, 65], crs=data_proj)
    grid = axis.gridlines(draw_labels=["left", "bottom"], dms=True)
    grid.xformatter = LONGITUDE_FORMATTER
    grid.yformatter = LATITUDE_FORMATTER


request = Request(
    collection=Collection(id='C2930725014-LARC_CLOUD'),
    spatial=BBox(-118.5393684093012, 34.1937592521836, -
                 118.52615242162526, 34.20474043035549),
    temporal={
        "start": dt.datetime(2024, 12, 1, 22, 30, 0),
        "stop": dt.datetime(2024, 12, 30, 22, 45, 0),
    },
)


job_id = harmony_client.submit(request)

print(f"jobID = {job_id}")
harmony_client.wait_for_processing(job_id, show_progress=True)

# Download the resulting files
results = harmony_client.download_all(job_id, directory="/tmp", overwrite=True)
all_results_stored = [f.result() for f in results]
