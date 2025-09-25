import pandas as pd
import geopandas as gpd
from shapely.geometry import box


df = pd.read_csv("/mnt/c/Users/abloom/Downloads/hourly_42602_2024.csv")
df['State Code'].drop_duplicates()
df.head()
df = df[(
                df['State Code'] == 6) 
             & (df['County Code'] == 37)
             & (df['Site Num'].isin([1201]))
                                      ]
df = df[['Latitude', 'Longitude', 'Site Num', 'State Code', 'County Code']]
df = df.drop_duplicates()
df.head()
df['geometry'] = gpd.points_from_xy(df.Longitude, df.Latitude)
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
gdf.head()

# --- Start of new code ---

# 1. Choose a projected CRS appropriate for your data's location
# We'll use GeoPandas' handy function to estimate the best UTM zone
projected_crs = gdf.estimate_utm_crs()
gdf_proj = gdf.to_crs(projected_crs)

# 2. Define the box dimensions in meters
# For a 1.2 km square, we need to go 600 meters in each direction from the center
half_side = 600  # 1200 meters / 2

# 3. Create the bounding box for each point in the projected CRS
# We apply a function to each geometry (point) in the projected GeoDataFrame
boxes = gdf_proj.geometry.apply(lambda point: box(
    point.x - half_side, 
    point.y - half_side, 
    point.x + half_side, 
    point.y + half_side
))

# 4. Create a new GeoDataFrame with these boxes and project it back to WGS84 (EPSG:4326)
boxes_gdf = gpd.GeoDataFrame(geometry=boxes, crs=projected_crs)
boxes_4326 = boxes_gdf.to_crs("EPSG:4326")

# 5. Extract the bounding box coordinates [min_lon, min_lat, max_lon, max_lat]
# The .bounds attribute gives us the coordinates we need
gdf['bbox'] = boxes_4326.bounds.values.tolist()

# Display the final result with the new 'bbox' column
gdf['bbox'].iloc[0]
gdf

gdf.to_file('/tmp/test.geojson', driver='GeoJSON')

pixel_size_degrees = (0.0001226401641466168225,-0.0001026835573264861556)
print("pixel_size_meters:", (pixel_size_degrees[0]*111320, pixel_size_degrees[1]*110540))



