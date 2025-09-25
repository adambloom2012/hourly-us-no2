import xarray as xr
import netCDF4
import geopandas as gpd
from shapely.geometry import box
file_path = "/mnt/c/Users/abloom/Downloads/sentinel-5p-epa/sentinel-5p/06-037-1201/l3_mean_monthly_US_large_2018_2020_005dg.netcdf"


ds = xr.open_dataset(file_path)

min_lon = ds.longitude.min().item()
max_lon = ds.longitude.max().item()
min_lat = ds.latitude.min().item()
max_lat = ds.latitude.max().item()

geometry = box(min_lon, min_lat, max_lon, max_lat)
# print geometry as text
print(geometry)
# save geometry to geojson
gdf = gpd.GeoDataFrame(geometry=[geometry], crs="EPSG:4326")
gdf.to_file('/tmp/s5p.geojson', driver='GeoJSON')