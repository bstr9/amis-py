import os

from .components.page import Page
from .exceptions import TypeInvalidError
from .web_server import App as WebApp
from .components.app import AppComponent

from logging import getLogger

logger = getLogger(__name__)


class App:
    def __init__(self, app=None, view=False):
        self.main = None
        self.pages = []
        self.router = {}
        self.view = view
        self.statics = {}
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
        if self.main:
            self.web.add_route("/main", self.main.render)
            print("main_page\t-\t/main")
        for page in self.pages:
            self.web.add_route(
                page.route,
                page.render)
            title = page.props.get("title") or hash(page)
            print(f"page:{title}\t-\t{page.route}")
            if self.view:
                view_route = page.route + "/view"
                self.web.add_route(view_route, page.page_view)
                print(f"page_view:{title}\t-\t{view_route}")
        if self.view:
            static_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "statics")
            self._load_static_files(static_path, static_path)
            # FIXME
            self.web.add_route(
                "/amis-py/static/{}/{filename}",
                self._get_static_file)
        self.web.run()

    def _get_static_file(self, filename):
        dirname = os.path.dirname(filename)

        # FIXME here
        def _get_file_from_path(name):
            full_name = dirname + name
            content = self.statics.get(full_name)
            if content:
                return content
            return ""

    def _load_static_files(self, root_path, static_path):
        for d in os.listdir(static_path):
            path = os.path.join(static_path, d)
            if os.path.isfile(path):
                with open(path, "r") as file:
                    context = file.read()
                filename = path.replace(root_path, "static")
                print(f"file:{filename}\t-\t" +
                      f"/amis-py/static/{filename}")
                self.statics[filename] = context
            else:
                self._load_static_files(root_path, path)
