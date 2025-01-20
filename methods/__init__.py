from . import auto_permanent
from . import auto_temporary
from .utils.args import encode_args
import flet as ft
import sys
import shlex
import subprocess

def run_script(script_path, *args, admin=True):
    command = ' '.join([script_path] + [shlex.quote(arg) for arg in args])
    pwsh_cmd = f"powershell -command \"Start-Process -WindowStyle Hidden -Wait '{sys.executable}' '{command}'"
    if admin:
        pwsh_cmd += " -Verb runas"
    pwsh_cmd += "\""
    proc = subprocess.run(pwsh_cmd, shell=True, check=True)
    return proc.returncode

def create_run_method(method):
    def run_method(config, log_path):
        return run_script(method.__file__, encode_args(config, log_path), admin=method.__METHOD_requires_admin__)
    return run_method

methods = [auto_temporary, auto_permanent]
available_methods = {method.__name__.split(".")[-1]: {
    "name": method.__METHOD_name__,
    "icon": ft.Icons[method.__METHOD_icon__],
    "description": method.__METHOD_description__,
    "script": method.__file__,
    "run_method": create_run_method(method)
} for method in methods}
