__version__ = "0.1"
import flet as ft
from app_pages import get_app_pages
from game_patchers import patch_methods

def main(page: ft.Page):
    # Initial configuration
    page.client_storage.set("patch_methods", patch_methods)
    if page.client_storage.get("patch_method") is None:
        page.client_storage.set("patch_method", "auto_permanent")
    page.theme_mode = page.client_storage.get("settings_theme")
    if page.theme_mode is None:
        page.theme_mode = "light"
    page.theme = ft.Theme(color_scheme_seed="#d11b52")
    page.window.min_width = 800
    page.window.min_height = 450
    page.window.width = 1020
    page.window.height = 660

    # Screen handler
    screen_list = get_app_pages(page)
    container = ft.Container(content=screen_list[0], expand=True)
    def set_screen(e):
        container.content = screen_list[e.control.selected_index]
        page.update()
    
    # Navrail
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        leading=ft.Text("rebelMC", size=24, weight=ft.FontWeight.BOLD),
        trailing=ft.Row([
            ft.Icon(ft.Icons.INFO_OUTLINE, size=16, weight=ft.FontWeight.W_200, color=ft.Colors.GREY),
            ft.VerticalDivider(width=2),
            ft.Text("version " + __version__, size=12, color=ft.Colors.GREY)
        ], spacing=1, alignment=ft.MainAxisAlignment.CENTER),
        group_alignment=-0.3,
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

    # Page content
    page.add(ft.Row([rail, ft.VerticalDivider(width=2), container], expand=True))
ft.app(main)
