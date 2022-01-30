from .components.page import Page
from .exceptions import TypeInvalidError
from .web_server import App as WebApp


class App:
    def __init__(self, app=None):
        self.pages = []
        self.router = {}
        if not app:
            self.web = WebApp()
        else:
            self.web = app

    def add(self, page):
        if not isinstance(page, Page):
            raise TypeInvalidError("must add page to app")
        self.pages.append(page)

    def run(self):
        for page in self.pages:
            view_hash = str(hash(page))
            self.web.add_route(
                "/page/{}".format(view_hash),
                page.render)
        self.web.run()
