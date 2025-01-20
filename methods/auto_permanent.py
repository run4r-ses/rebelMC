__METHOD_name__ = "Auto-patched Permanent DLL"
__METHOD_icon__ = "FILE_OPEN"
__METHOD_description__ = "Automatically patches Store DLL from file, and writes it permanently to disk."
__METHOD_requires_admin__ = True
if __name__ == "__main__":
    from utils.log import MethodLogger
    from utils.args import decode_args
else:
    from .utils.log import MethodLogger
    from .utils.args import decode_args
import time
import sys

def main(args):
    config, log_path = decode_args(args)
    logger = MethodLogger(log_path)

    logger.debug("TODO: Implement method")
    logger.debug("Sleeping for 3 seconds and exiting")
    time.sleep(3)
    return 0

if __name__ == "__main__":
    main(sys.argv[1])
