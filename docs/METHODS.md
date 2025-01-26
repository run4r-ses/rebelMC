# Method handling in rebelMC

rebelMC has support for method files, which are located in `src/rebelmc/methods/`. Each method is a Python script that is isolated from the program.

## Method attributes
Each method has attributes defined in the file like so:
```py
__METHOD_name__ = "Example method"
__METHOD_icon__ = "QUESTION_MARK"
__METHOD_description__ = "This is an example method."
__METHOD_requires_admin__ = True
__METHOD_actions__ = ["patch", "uninstall"]
```
The attributes are as such:
- `__METHOD_name__`: Name of the method.
- `__METHOD_icon__`: Icon name for the method, all icons can be found [here](https://flet.dev/docs/reference/icons/).
- `__METHOD_description__`: A description of the method.
- `__METHOD_requires_admin__`: Whether or not the method requires UAC elevation to function.
- `__METHOD_actions__`: List of actions the method provides.

## Running a method
**NOTE:** Run methods are incompatible with PyInstaller and other packaging tools, please see "Packaging notice" in the [installation guide](/docs/INSTALL.md#packaging-notice) for more information.

Each method has a "run method" to allow interacting with the method. A run method does the following:
- Takes in **action**, **configuration *(aka. app settings)***, and **log file path**
- Pickles config and log path & encodes as base64 to pass through command line *(using `.utils.args`)*
- Creates a `Start-Process` instance where the method is launched as a seperate Python instance
- Returns process instance and a termination function

Run methods are the *only way* that a method supports interaction. Any other usage of methods are unsupported.

## Method actions
Each method can implement an action that can be triggered. The available actions are as such:
- `patch` - Start Patch
- `Uninstall` - Uninstall Patch

Each action is defined as a function, and is executed by the script accordingly.
All actions parse arguments and configure a logging instance *(using `.utils`)*, and they can be viewed as a varying `main` function when compared with regular Python scripts.

### Running an action
When the method script is executed with a run method, the method will parse arguments and run the corresponding action as seen in the example below:
```py
if __name__ == "__main__":
    run_type = sys.argv[1] # This is the action
    method = lambda x: None
    if run_type == "patch":
        method = __METHOD_patch__ # This is a "patch" action
    if run_type == "uninstall":
        method = __METHOD_uninstall__ # This is an "uninstall" action
    sys.exit(method(sys.argv[2])) # argv[2] is the "args" for the action
```

### Implementing an action
To implement a basic action, the required utilities must be first imported:
```py
from utils.log import MethodLogger
from utils.args import decode_args
```

Then, define a function header and parse arguments:
```py
from utils.log import MethodLogger
from utils.args import decode_args

def __METHOD_patch__(args):
    config, log_path = decode_args(args)
    logger = MethodLogger(log_path)
```

Finally, add some basic logic, and you're done!
```py
def __METHOD_patch__(args):
    config, log_path = decode_args(args)
    logger = MethodLogger(log_path)

    logger.info("This is my action!")
    logger.debug("Sleeping for 3 seconds and exiting")
    time.sleep(3)
    return 0
```

These are the very basics of implementing an action. Any kind of code can be written here.

### Logging and return values
For logging, `MethodLogger` from `.utils.log` is used. This can be used just like a `Logger` object from `logging`.

Although it is not recommended to do so, you can access the log file directly from `logger.log_file`.

For return values, these are the supported values:
- `0` - Success
- `1` - Failure

These values can be just returned as an integer. Any other value will display "Finished" instead.
