from .utils.args import encode_args
from pathlib import Path
import ast
import flet as ft
import sys
import shlex
import subprocess

def run_script(script_path, *args, admin=False):
    command = ' '.join([f'\\"{script_path}\\"'] + [shlex.quote(arg) for arg in args])
    pwsh_cmd = (
        f'powershell -command "& {{ '
        f'$process = Start-Process \'{sys.executable}\' -ArgumentList \'{command}\' -WindowStyle Hidden -PassThru -Wait'
        f'{" -Verb runas" if admin else ""}'
        f'; exit $process.ExitCode; }}"'
    )
    proc = subprocess.run(pwsh_cmd, shell=True)
    return proc.returncode
 
def create_run_method(method_file, needs_admin):
    def run_method(action, config, log_path):
        return run_script(method_file, action, encode_args(config, log_path), admin=needs_admin)
    return run_method

def lazy_getattrs(module_path, attr_names):
    module_path = Path(module_path)
    if not module_path.is_file():
        raise FileNotFoundError(f"No file found at {module_path}")
    with module_path.open("r") as f:
        tree = ast.parse(f.read(), filename=str(module_path))

    attrs = {}
    missing = attr_names.copy()
    for node in tree.body:
        if not missing:
            break
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            attr = node.targets[0].id
            if attr in attr_names:
                attrs[attr] = ast.literal_eval(node.value)
                missing.remove(attr)
    if missing:
        raise AttributeError(f"Method is missing attributes {', '.join(missing)}")
    return attrs

def parse_method(module_path):
    required_attrs = [
        "__METHOD_name__",
        "__METHOD_icon__",
        "__METHOD_description__",
        "__METHOD_requires_admin__",
        "__METHOD_actions__",
    ]
    module = lazy_getattrs(module_path, required_attrs)
    return {
        "name": module["__METHOD_name__"],
        "icon": ft.Icons[module["__METHOD_icon__"]],
        "description": module["__METHOD_description__"],
        "script": module_path,
        "run_method": create_run_method(
            module_path,
            module["__METHOD_requires_admin__"]
        ),
        "actions": module["__METHOD_actions__"],
    }

def get_available_methods():
    base_path = Path(__file__).resolve().parent
    method_files = [
        f.resolve() for f in base_path.iterdir()
        if f.is_file() and f.suffix == ".py" and not f.stem.startswith("_")
    ]

    available_methods = {}
    for file in method_files:
        available_methods[file.stem] = parse_method(str(file))

    return available_methods
