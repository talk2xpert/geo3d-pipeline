import logging


def setup_logger(verbose):
   level = logging.INFO if verbose else logging.WARNING
   logging.basicConfig(
       level=level,
       format="%(asctime)s [%(levelname)s] %(message)s"
   )
