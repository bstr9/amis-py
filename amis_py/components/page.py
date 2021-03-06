from ..exceptions import TypeInvalidError
from .base import Prop, Properties, BaseComponent


class PageProperties(Properties):
    # do not support remark, aside, toolbar and initApi now
    def __init__(self, *args, **kwargs):
        super().__init__()
        defaults = [
            Prop("title", str, ""),
            Prop("sub_title", str, ""),
            Prop("class_name", str, "", "className"),
        ]
        self.update_defaults(defaults)
        self.update_properties(**kwargs)


class Page(BaseComponent):
    def __init__(self, props=PageProperties()):
        super().__init__(props)
        self._view = {
            "type": "page",
            "body": []
        }
        self.create()
        if not isinstance(self.data, dict):
            raise TypeInvalidError(
                "component Form can't accept data with type"
                "{}".format(type(self.data)))

        view = self.view()
        if not isinstance(view, dict):
            raise TypeInvalidError(
                "component Form can't accept view with type"
                "{}".format(type(view)))
        self._view.update(props.properties)
        for _, component in view.items():
            self.add(component)

    def add(self, component: BaseComponent):
        if not hasattr(component, "render"):
            raise TypeInvalidError(
                "set invalid component {} as view".format(
                    component.__class__.__name__
                )
            )
        self._view.get("body").append(component.render())
        return self
