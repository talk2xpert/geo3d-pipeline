import rasterio


def get_base_height(cfg, geom):
   if not cfg["terrain"]["enable"]:
       return 0

   path = cfg["terrain"]["dtm_path"]

   with rasterio.open(path) as src:
       x, y = geom.centroid.x, geom.centroid.y
       for val in src.sample([(x, y)]):
           return float(val[0])

   return 0
