from shapely.ops import unary_union


def preprocess(gdf, cfg):
   if cfg["processing"]["clean_geometry"]:
       gdf["geometry"] = gdf["geometry"].buffer(0)

   gdf = gdf[gdf.geometry.area > cfg["processing"]["min_area"]]
   return gdf


def get_geometries(gdf, cfg):
   if cfg["processing"]["merge_overlaps"]:
       merged = unary_union(gdf.geometry)
       return [merged] if merged.geom_type == "Polygon" else list(merged.geoms)

   return list(gdf.geometry)
