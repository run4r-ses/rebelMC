__METHOD_name__ = "In-memory Patching"
__METHOD_icon__ = "AUTO_FIX_HIGH"
__METHOD_description__ = "Automatically patches Store DLL from game, and injects it back."
from .utils import MethodLogger
import time

def main(config, log_path):
    logger = MethodLogger(log_path)
    logger.debug("TODO: Implement method")
    logger.debug("Sleeping for 3 seconds")
    time.sleep(3)
    logger.debug("Sleeping for 2 seconds")
    time.sleep(2)
    logger.debug("Done, exiting")
    pass
