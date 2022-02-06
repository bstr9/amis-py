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
    def __init__(self, props: PageGroupProperties):
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
        self._view.update(props.properties)


"""
example:
    group = PageGroup(PageGroupProperties(title="hello")
    page = Page(PageGroupProperties(title="hello").add(From())
    group.add(page, title="hello")
    group.add(page, title="???")
"""
