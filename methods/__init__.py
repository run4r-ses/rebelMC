from . import auto_permanent
from . import auto_temporary
import flet as ft

methods = [auto_temporary, auto_permanent]
available_methods = {method.__name__.split(".")[-1]: {
    "name": method.__METHOD_name__,
    "icon": ft.Icons[method.__METHOD_icon__],
    "description": method.__METHOD_description__,
    "func": method.main,
} for method in methods}
