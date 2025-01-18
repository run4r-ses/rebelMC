import flet as ft

def view(page):
    def change_theme(e):
        page.theme_mode = "dark" if e.control.value else "light"
        page.client_storage.set("settings_theme", page.theme_mode)
        page.update()

    general_section = [
        ft.Text("General", size=24, weight=ft.FontWeight.BOLD),
        ft.Container(height=2),
        ft.Switch(value=True if page.theme_mode == "dark" else False, label="Use dark mode", on_change=change_theme),
        ft.Switch(value=False, label="Close after patching",
                  on_change=lambda e: page.client_storage.set("settings_exitafter", e.control.value)),
    ]

    mc_section = [
        ft.Text("Minecraft Settings", size=24, weight=ft.FontWeight.BOLD),
        ft.Container(height=2),
        ft.Switch(value=False, label="Start game automatically after patching",
                  on_change=lambda e: page.client_storage.set("settings_start", e.control.value)),
    ]
    
    sections = [general_section, mc_section]
    content = []
    for i, section in enumerate(sections):
        for item in section:
            content.append(item)
        if i < len(sections) - 1:
            content.append(ft.Divider())
    return ft.Column(
        content,
        alignment=ft.MainAxisAlignment.START,
        expand=True,
    )
