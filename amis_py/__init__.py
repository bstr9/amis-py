from .components.page import Page
from .exceptions import TypeInvalidError


class App:
    def __init__(self, app=None):
        self.pages = []

    def add(self, page):
        if not isinstance(page, Page):
            raise TypeInvalidError("must add page to app")
        self.pages.append(page)

    def run(self):
        pass
