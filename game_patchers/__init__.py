from . import auto_permanent
from . import auto_temporary
import flet as ft

patchers = [auto_temporary, auto_permanent]
patch_methods = {patcher.__name__.split(".")[-1]: {
    "name": patcher.__METHOD_name__,
    "icon": ft.Icons[patcher.__METHOD_icon__],
    "description": patcher.__METHOD_description__,
    "func": patcher.main,
} for patcher in patchers}
