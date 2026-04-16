import argparse
import yaml
import logging
import os

from src.io_utils import load_data
from src.geometry import preprocess, get_geometries
from src.extrusion import build_mesh
from src.slicing import slice_building
from src.terrain import get_base_height
from src.utils import setup_logger


def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def run(cfg):
    setup_logger(cfg["performance"]["verbose"])

    os.makedirs(cfg["output"]["out_dir"], exist_ok=True)

    gdf = load_data(cfg)
    gdf = preprocess(gdf, cfg)

    geometries = get_geometries(gdf, cfg)

    for i, geom in enumerate(geometries, start=1):
        logging.info(f"Processing Building {i}")

        base_z = get_base_height(cfg, geom)

        mesh_data = build_mesh(gdf, geom, cfg, i, base_z)

        slice_building(mesh_data, cfg, i)

    logging.info("Pipeline execution completed ✔")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    run(config)
