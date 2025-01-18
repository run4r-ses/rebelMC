from .patch import view as patch
from .methods import view as methods
from .settings import view as settings

def get_app_pages(page):
    return [patch(page), methods(page), settings(page)]
