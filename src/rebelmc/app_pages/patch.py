import flet as ft
import os
import time
import threading
from datetime import datetime

def view(page):
    # Logging handlers
    log_thread_running = False

    def read_log_thread(log_file_name):
        global log_thread_running
        last_modified = 0
        with open(log_file_name, "r") as file:
            while log_thread_running:
                current_modified = os.path.getmtime(log_file_name)
                if current_modified != last_modified:
                    file.seek(0)
                    content = file.read()
                    text_box.value = content
                    last_modified = current_modified
                    page.update()
                time.sleep(0.1)

    def create_log_file(method_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = page.log_dir / f"{timestamp}_{method_name}.log"
        log_file.touch()
        return str(log_file.resolve())


    # Method handler
    def run_method(action, method_name, log_filename):
        global log_thread_running
        method = page.patch_methods[method_name]
        return_code = method["method"](action, page.client_storage.get("settings"), log_filename)
        if return_code == 0:
            status_title.value = "Success"
        elif return_code == 1:
            status_title.value = "Failure"
        else:
            status_title.value = "Finished"
        log_thread_running = False
        go_back_button.disabled = False
        page.update()
        status_title.value = "Executing..."
        go_back_button.disabled = True
        text_box.value = ""
        log_thread_running = False


    # Start & Home button handler
    def start_action(action):
        method_name = page.client_storage.get("patch_method")
        log_file = create_log_file(method_name)
        current_container.content = action_content
        page.update()
        global log_thread_running
        log_thread_running = True
        threading.Thread(target=read_log_thread, args=(log_file,), daemon=True).start()
        threading.Thread(target=run_method, args=(action, method_name, log_file), daemon=True).start()

    def homepage(e):
        generate_page_content()
        current_container.content = page_content
        page.update()


    # Main page
    available_actions = [
        # (id, button text, action title)
        ("patch", "Patch", "Start Patch"),
        ("uninstall", "Uninstall", "Uninstall Patch"),
    ]
    def generate_page_content():
        page_items = []
        method_actions = page.patch_methods[page.client_storage.get("patch_method")]["actions"]
        for (action, button_text, display_name) in available_actions:
            page_items.append(ft.Text(display_name, size=24, weight=ft.FontWeight.BOLD))
            action_button = ft.ElevatedButton()
            if action in method_actions:
                action_button.text = f"\t\t{button_text}\t\t"
                action_button.on_click = lambda e, a=action: start_action(a)
            else:
                action_button.text = "\t\tNot available for method\t\t"
                action_button.disabled = True
            page_items.append(action_button)
        global page_content
        page_content = ft.Column(
            page_items,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    generate_page_content()

    # Log page
    status_title = ft.Text(
        value="Executing...",
        size=24,
        weight=ft.FontWeight.BOLD
    )
    text_box = ft.Text(
        value="",
        font_family="Roboto Mono",
        text_align=ft.TextAlign.LEFT,
        expand=True
    )
    text_container = ft.Column(
        [text_box],
        width=800,
        height=400,
        alignment=ft.MainAxisAlignment.START,
        scroll=True
    )
    go_back_button = ft.ElevatedButton("Go Back", on_click=homepage, disabled=True)

    action_content = ft.Column(
        [status_title, text_container, go_back_button],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )


    # Method update checking
    current_container = ft.Container(content=page_content)
    def check_patch_method():
        last_patch_method = page.client_storage.get("patch_method")
        while True:
            current_patch_method = page.client_storage.get("patch_method")
            if current_patch_method != last_patch_method:
                last_patch_method = current_patch_method
                generate_page_content()
                if not log_thread_running:
                    current_container.content = page_content
                    page.update()
            time.sleep(0.1)
    threading.Thread(target=check_patch_method, daemon=True).start()


    # View content
    info_text = ft.Row(
        [
            ft.Icon(ft.Icons.INFO_OUTLINE, size=16, weight=ft.FontWeight.W_200, color=ft.Colors.GREY),
            ft.VerticalDivider(width=2),
            ft.Text(
                "This software is in an early phase, and may not function as expected",
                size=12,
                color=ft.Colors.GREY
            )
        ],
        spacing=1,
        alignment=ft.MainAxisAlignment.CENTER
    )

    return ft.Column(
        [
            current_container,
            info_text
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
