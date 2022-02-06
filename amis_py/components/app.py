from .page import Page
from .exceptions import TypeInvalidError
from .base import Prop, Properties, BaseComponent


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
            if not isinstance(component, Page):
                raise TypeInvalidError(
                    "can not set type {} "
                    "as sub page in app".format(
                        type(component)))
            self.add(component)

    def add(self, component: Page):
        if not isinstance(component, Page):
            raise TypeInvalidError(
                "can not set type {} "
                "as sub page in app".format(
                    type(component)))
        self._view.get("pages").append(component.render())
        return self
