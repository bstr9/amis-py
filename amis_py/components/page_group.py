from .page import Page
from ..exceptions import TypeInvalidError
from .base import Prop, Properties, BaseComponent


class PageGroupProperties(Properties):
    def __init__(self, *args, **kwargs):
        super().__init__()
        defaults = [
            Prop("title", str, "title"),
        ]
        self.update_defaults(defaults)
        self.update_properties(**kwargs)


class PageGroup(BaseComponent):
    """
    Example1:
        group = PageGroup(PageGroupProperties(title="hello")
        page = Page(PageGroupProperties(title="hello").add(From())
        group.add(page, title="hello")

    Example2:
        page = Page(PageGroupProperties(title="hello").add(From())
        class TestPageGroup(PageGroup):
            def view(self):
                return {
                    "test_page1": page,
                    "test_page2": page
                }
        page_group = TestPageGroup(PageGroupProperties(title="hello"))
    """
    def __init__(self, props: PageGroupProperties = PageGroupProperties()):
        super().__init__(props)
        self._view = {
            "children": []
        }
        self.create()
        view = self.view()
        if not isinstance(view, dict):
            raise TypeInvalidError(
                "component Form can't accept view with type"
                "{}".format(type(view)))
        for title, page in view.items():
            self.add(page, title)
        self._view.update(props.properties)

    def add(self, page: Page, title: str = ""):
        if not isinstance(page, Page):
            raise TypeInvalidError("please add page instance to page group")
        if not isinstance(title, str):
            raise TypeInvalidError("please use string as page title")

        if not title:
            title = page.props.get("title")
        self._view.get("children").append({
            "label": title,
            "schema": page.render()
        })
