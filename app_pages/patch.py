import flet as ft
import os
import time
import threading
from datetime import datetime

def view(page):
    log_thread_running = False

    def read_file_thread(file_path):
        global log_thread_running
        last_modified = 0
        with open(file_path, 'r') as file:
            while log_thread_running:
                current_modified = os.path.getmtime(file_path)
                if current_modified != last_modified:
                    file.seek(0)
                    content = file.read()
                    text_box.value = content
                    last_modified = current_modified
                    page.update()
                time.sleep(0.1)

    def create_log_file(method_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"./{timestamp}_{method_name}.log"
        with open(log_filename, 'w') as log_file:
            #log_file.write(f"Log created at {timestamp} with method {method_name}")
            pass
        return log_filename

    def run_method(method_name, log_filename):
        method = page.patch_methods[method_name]
        method["func"](page.client_storage.get("settings"), log_filename)
        go_back_button.disabled = False

    def start_patch(e):
        # Start logging
        method_name = page.client_storage.get("patch_method")
        log_filename = create_log_file(method_name)
        patch_button.visible = False
        go_back_button.visible = True
        page.update()
        global log_thread_running
        log_thread_running = True
        threading.Thread(target=read_file_thread, args=(log_filename,), daemon=True).start()
        threading.Thread(target=run_method, args=(method_name, log_filename), daemon=True).start()

    def reset_page(e):
        go_back_button.visible = False
        go_back_button.disabled = True
        patch_button.visible = True
        text_box.value = ""
        global log_thread_running
        log_thread_running = False
        page.update()


    patch_button = ft.ElevatedButton("Patch", on_click=start_patch)
    go_back_button = ft.ElevatedButton("Go Back", on_click=reset_page, visible=False, disabled=True)
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
        scroll=True
    )

    return ft.Column(
        [
            ft.Text("Patch", size=24, weight=ft.FontWeight.BOLD),
            patch_button,
            text_container,
            go_back_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
