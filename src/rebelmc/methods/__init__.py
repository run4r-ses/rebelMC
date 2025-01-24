from . import auto_permanent
from . import auto_temporary
from .utils.args import encode_args
import flet as ft
import sys
import shlex
import subprocess

def run_script(script_path, *args, admin=True):
    command = ' '.join([f'\\"{script_path}\\"'] + [shlex.quote(arg) for arg in args])
    pwsh_cmd = (
        f'powershell -command "& {{ '
        f'$process = Start-Process \'{sys.executable}\' -ArgumentList \'{command}\' -WindowStyle Hidden -PassThru -Wait'
        f'{" -Verb runas" if admin else ""}'
        f'; exit $process.ExitCode; }}"'
    )
    proc = subprocess.run(pwsh_cmd, shell=True)
    return proc.returncode

def create_run_method(method):
    def run_method(action, config, log_path):
        return run_script(method.__file__, action, encode_args(config, log_path), admin=method.__METHOD_requires_admin__)
    return run_method

methods = [auto_temporary, auto_permanent]
available_methods = {method.__name__.split(".")[-1]: {
    "name": method.__METHOD_name__,
    "icon": ft.Icons[method.__METHOD_icon__],
    "description": method.__METHOD_description__,
    "script": method.__file__,
    "method": create_run_method(method),
    "actions": method.__METHOD_actions__
} for method in methods if not method.__name__.startswith("_")}
