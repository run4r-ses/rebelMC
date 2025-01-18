import flet as ft

def view(page):
    methods = page.client_storage.get("patch_methods")

    def get_header(method):
        return [
            ft.Icon(method.get("icon", ft.Icons.INFO_OUTLINE), size=96),
            ft.Column(
                controls=[
                    ft.Text(method["name"], size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(method["description"], size=14),
                ],
                alignment=ft.MainAxisAlignment.START, expand=True,
            ),
        ]
    def change_method(e):
        page.client_storage.set("patch_method", e.control.value)
        header.content.controls = get_header(methods[e.control.value])
        page.update()

    
    default_value = page.client_storage.get("patch_method")
    header = ft.Container(
        padding=ft.padding.symmetric(horizontal=100, vertical=30),
        content=ft.Row(controls=get_header(methods[default_value]))
    )
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=100, vertical=30),
        content=ft.Column(
            controls=[
                header,
                ft.Dropdown(
                    value=page.client_storage.get("patch_method"),
                    options=[ft.dropdown.Option(name, methods[name]["name"]) for name in methods.keys()],
                    on_change=change_method
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
    )