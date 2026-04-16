import trimesh
from shapely.geometry import Polygon


def extrude(poly, height, base):
   mesh = trimesh.creation.extrude_polygon(poly, height)
   mesh.apply_translation([0, 0, base])
   return mesh


def scale_polygon(poly, ratio):
   c = poly.centroid
   coords = [(c.x + (x - c.x)*ratio, c.y + (y - c.y)*ratio)
             for x, y in poly.exterior.coords]
   return Polygon(coords)


def build_mesh(gdf, poly, cfg, idx, base_z):

   base_height = cfg["extrusion"]["base_height_default"]

   base_mesh = extrude(poly, base_height, base_z)

   partial_poly = scale_polygon(poly, cfg["extrusion"]["coverage_ratio"])

   upper_mesh = extrude(
       partial_poly,
       cfg["extrusion"]["upper_height"],
       base_z + base_height
   )

   full = trimesh.util.concatenate([base_mesh, upper_mesh])

   return {
       "base": base_mesh,
       "upper": upper_mesh,
       "full": full
   }
