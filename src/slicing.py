import trimesh
import os


def slice_mesh(mesh, floor_height, total_height):
   floors = []
   z = 0
   i = 1

   while z < total_height:
       top = min(z + floor_height, total_height)

       box = trimesh.creation.box(
           extents=[10000, 10000, top - z],
           transform=trimesh.transformations.translation_matrix(
               [0, 0, z + (top - z)/2]
           )
       )

       sliced = mesh.intersection(box)

       if sliced and not sliced.is_empty:
           floors.append((i, sliced))

       z = top
       i += 1

   return floors


def slice_building(mesh_data, cfg, idx):

   out = cfg["output"]["out_dir"]
   prefix = os.path.join(out, f"{cfg['output']['prefix']}_{idx}")

   # Export full
   mesh_data["full"].export(prefix + "_full.obj")

   if not cfg["slicing"]["export_per_floor"]:
       return

   base_floors = slice_mesh(
       mesh_data["base"],
       cfg["slicing"]["floor_height"],
       cfg["extrusion"]["base_height_default"]
   )

   upper_floors = slice_mesh(
       mesh_data["upper"],
       cfg["slicing"]["floor_height"],
       cfg["extrusion"]["upper_height"]
   )

   for fno, m in base_floors:
       m.export(prefix + f"_base_floor_{fno}.obj")

   for fno, m in upper_floors:
       m.export(prefix + f"_upper_floor_{fno}.obj")
