import flet as ft

default_settings = {
    "theme": "light",
    "exit_after": False,
    "start_game": True,
    "use_preview": False
}

def view(page):
    get_setting = lambda x: page.client_storage.get("settings").get(x)
    def update_setting(setting_name, value):
        current_settings = page.client_storage.get("settings")
        current_settings[setting_name] = value
        page.client_storage.set("settings", current_settings)

    def change_theme(e):
        page.theme_mode = "dark" if e.control.value else "light"
        update_setting("theme", page.theme_mode)
        page.update()

    general_section = [
        ft.Text("General", size=24, weight=ft.FontWeight.BOLD),
        ft.Container(height=2),
        ft.Switch(value=True if page.theme_mode == "dark" else False, label="Use dark mode", on_change=change_theme),
        ft.Switch(value=get_setting("exit_after"), label="Close after patching",
                  on_change=lambda e: update_setting("exit_after", e.control.value)),
    ]

    mc_section = [
        ft.Text("Minecraft Settings", size=24, weight=ft.FontWeight.BOLD),
        ft.Container(height=2),
        ft.Switch(value=get_setting("start_game"), label="Start game automatically",
                  on_change=lambda e: update_setting("start_game", e.control.value)),
        ft.Switch(value=get_setting("use_preview"), label="Patch Minecraft Preview instead of Minecraft release (only applicable to non-system methods)",
                  on_change=lambda e: update_setting("use_preview", e.control.value)),
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
