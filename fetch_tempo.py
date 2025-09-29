import helper
import sys
import datetime as dt
from IPython.display import display, JSON
import rasterio
import rasterio.plot
import netCDF4 as nc4
from matplotlib import pyplot as plt
import numpy as np

from harmony import BBox, Client, Collection, Request, Environment


harmony_client = Client(env=Environment.UAT)

collection = Collection(auth=)

request = Request(
    collection=collection,
    spatial=BBox(-165, 52, -140, 77),
    temporal={
        'start': dt.datetime(2010, 1, 1),
        'stop': dt.datetime(2020, 12, 30)
    },
    variables=['blue_var'],
    max_results=10,
    crs='EPSG:4326',
    format='image/tiff',
    height=512,
    width=512
)

request.is_valid()
