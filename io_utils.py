import zipfile
import tempfile
import os
import geopandas as gpd


def extract_zip(zip_path):
   temp_dir = tempfile.mkdtemp()
   with zipfile.ZipFile(zip_path, 'r') as z:
       z.extractall(temp_dir)
   return temp_dir


def find_shp(folder):
   for f in os.listdir(folder):
       if f.endswith(".shp"):
           return os.path.join(folder, f)
   raise Exception("Shapefile not found")


def load_data(cfg):
   folder = extract_zip(cfg["input"]["zip_path"])
   shp = find_shp(folder)
   gdf = gpd.read_file(shp)

   if gdf.crs and gdf.crs.is_geographic:
       gdf = gdf.to_crs(epsg=cfg["input"]["crs_projected"])

   return gdf
