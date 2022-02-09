from .components.page import Page
from .exceptions import TypeInvalidError
from .web_server import App as WebApp
from .components.app import AppComponent


class App:
    def __init__(self, app=None):
        self.main = None
        self.pages = []
        self.router = {}
        if not app:
            self.web = WebApp()
        else:
            self.web = app

    def add(self, main):
        if isinstance(main, Page):
            self.pages.append(main)
        elif isinstance(main, AppComponent):
            self.main = main
        else:
            raise TypeInvalidError(
                "must add page component or app component")

    def run(self):
        for page in self.pages:
            view_hash = str(hash(page))
            self.web.add_route(
                "/page/{}".format(view_hash),
                page.render)
        if self.main:
            self.web.add_route("/main", self.main.render)
        self.web.run()
