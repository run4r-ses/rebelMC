import flet as ft

def view(page):
    return ft.Column(
        [ft.Text("TODO", size=48, weight=ft.FontWeight.BOLD)],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
