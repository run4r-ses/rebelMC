__METHOD_name__ = "Auto-patched Permanent DLL"
__METHOD_icon__ = "FILE_OPEN"
__METHOD_description__ = "Automatically patches Store DLL from file, and writes it permanently to disk."
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
