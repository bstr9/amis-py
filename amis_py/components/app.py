from .page import Page
from .page_group import PageGroup
from .base import Prop, Properties, BaseComponent
from ..exceptions import TypeInvalidError

from typing import Union


class AppProperties(Properties):
    def __init__(self, *args, **kwargs):
        super().__init__()
        defaults = [
            Prop("brand_name", str, "brandName"),
            Prop("logo", str, ""),
        ]
        self.update_defaults(defaults)
        self.update_properties(**kwargs)


class App(BaseComponent):
    def __init__(self, props):
        super().__init__(props)
        self._view = {
            "type": "app",
            "pages": []
        }
        self.create()
        view = self.view()
        if not isinstance(view, dict):
            raise TypeInvalidError(
                "component Form can't accept view with type"
                "{}".format(type(view)))
        self._view.update(props.properties)
        for _, component in view.items():
            self.add(component)

    def add(self, component: Union[Page, PageGroup]):
        if isinstance(component, PageGroup):
            self._view.get("pages").append(component.render())
        elif isinstance(component, Page):
            last_group = None
            for item in self._view.get("pages").reverse():
                if isinstance(item):
                    last_group = item
                    break
            if not last_group:
                last_group = PageGroup()
            last_group.add(component)
            self._view.get("pages").append(last_group)
        else:
            raise TypeInvalidError(
                "can not set type {} "
                "as sub page in app".format(
                    type(component)))
        return self
