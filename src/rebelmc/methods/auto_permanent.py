__METHOD_name__ = "Auto-patched Permanent DLL"
__METHOD_icon__ = "FILE_OPEN"
__METHOD_description__ = "Automatically patches Store DLL from file, and writes it permanently to disk."
__METHOD_requires_admin__ = True
__METHOD_actions__ = ["patch", "uninstall"]

from utils.log import MethodLogger
from utils.args import decode_args
import time
import sys

def __METHOD_patch__(args):
    config, log_path = decode_args(args)
    logger = MethodLogger(log_path)

    logger.debug("TODO: Implement method")
    logger.debug("Sleeping for 3 seconds and exiting")
    time.sleep(3)
    return 0

def __METHOD_uninstall__(args):
    config, log_path = decode_args(args)
    logger = MethodLogger(log_path)

    logger.debug("TODO: Implement uninstall")
    logger.debug("Sleeping for 3 seconds and exiting")
    time.sleep(3)
    return 0 


if __name__ == "__main__":
    run_type = sys.argv[1]
    method = lambda x: None
    if run_type == "patch":
        method = __METHOD_patch__
    if run_type == "uninstall":
        method = __METHOD_uninstall__
    sys.exit(method(sys.argv[2]))
