__version__ = "0.5rc1"
import argparse
import flet as ft
from pathlib import Path
from .app_pages import get_app_pages
from .app_pages.settings import configure_default_settings
from .methods import get_available_methods

def app(page: ft.Page, args):
    # Initial configuration
    base_path = Path(__file__).resolve().parent
    configure_default_settings(page)
    page.patch_methods = get_available_methods()
    if args.log_dir is not None:
        page.log_dir = Path(args.log_dir)
        page.log_dir.mkdir(parents=True, exist_ok=True)
    else:
        page.log_dir = Path(".")
    page.theme = ft.Theme(color_scheme_seed="#ff1c6b")
    page.window.min_width = 800
    page.window.min_height = 450
    page.window.width = 1020
    page.window.height = 660
    page.fonts = {
        "Roboto Mono": str(base_path / "assets" / "RobotoMono.ttf"),
    }

    # Screen handler
    screen_list = get_app_pages(page)
    container = ft.Container(content=screen_list[0], expand=True)
    def set_screen(e):
        container.content = screen_list[e.control.selected_index]
        page.update()
    
    # App logo
    def update_logo():
        page.logo.src = str(base_path / f"assets/logo_{page.theme_mode}.png")
    page.update_logo = update_logo
    page.logo = ft.Image(
        width=50,
        height=50,
    )
    page.update_logo()

    # Navrail
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=ft.Container(content=page.logo, padding=20),
        trailing=ft.Row([
            ft.Icon(ft.Icons.INFO_OUTLINE, size=16, weight=ft.FontWeight.W_200, color=ft.Colors.GREY),
            ft.VerticalDivider(width=2),
            ft.Text("version " + __version__, size=12, color=ft.Colors.GREY)
        ], spacing=1, alignment=ft.MainAxisAlignment.CENTER),
        group_alignment=-(1/3),
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.BUILD_OUTLINED,
                selected_icon=ft.Icons.BUILD,
                label="Patch",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_SUGGEST_OUTLINED,
                selected_icon=ft.Icons.SETTINGS_SUGGEST,
                label="Methods",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Settings",
            ),
        ],
        on_change=set_screen
    )

    # Exit patching check
    def handle_window_event(e):
        if e.data == "close":
            if page.patch_process is not None:
                page.open(confirm_dialog)
            else:
                page.window.visible = False
                page.window.destroy()
    page.patch_process = None
    page.window.prevent_close = True
    page.window.on_event = handle_window_event

    def terminate_proc(e):
        if page.patch_process is not None:
            page.patch_process[1]()
        page.window.visible = False
        page.window.destroy()
    def close_dialog(e):
        page.close(confirm_dialog)
    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Patch is still running"),
        content=ft.Text((
            "Exiting now will kill the process, "
            "which can lead to unexpected behavior.\n"
            "Are you sure you want to exit?"
        )),
        actions=[
            ft.ElevatedButton("Yes", on_click=terminate_proc),
            ft.OutlinedButton("No", on_click=close_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Page content
    page.add(ft.Row([rail, ft.VerticalDivider(width=2), container], expand=True))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--log_dir", 
        type=str, 
        default=None,
        help="Directory to save log files to"
    )
    args = parser.parse_args()
    ft.app(lambda page: app(page, args))

if __name__ == "__main__":
    main()
