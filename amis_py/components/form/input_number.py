from .form_item import FormItem
from .properties import FormItemProperties
from amis_py.components.base import Prop


class InputNumberProperties(FormItemProperties):
    def __init__(self, *args, **kwargs):
        super().__init__()
        defaults = [
            Prop("min_value", int, None, "min"),
            Prop("max_value", int, None, "max"),
            Prop("step", int, None),
            Prop("precision", float, None),
            Prop("show_steps", int, None, "showSteps"),
            Prop("prefix", str, ""),
            Prop("suffix", str, ""),
            Prop("kilobit_separator", int, None, "kilobitSeparator"),
            Prop("unit_options", list, None, "unitOptions"),
            Prop("value", int, None)
        ]
        self.update_defaults(defaults)
        self.update_properties(**kwargs)


class InputNumber(FormItem):
    def __init__(
        self, props: InputNumberProperties = InputNumberProperties()
    ):
        super().__init__(props)
        self._type = "input-number"
        self._view = {
            "type": self._type,
        }
        self._view.update(props.properties)
        if not props.get("name"):
            self._view["name"] = props.get("label")

    @property
    def name(self):
        return self._view.get("name")

    @name.setter
    def name(self, name):
        self._view["name"] = name
        if self._view.get("label") == "":
            self._view["label"] = name

    @property
    def value(self):
        return self._view.get("value")

    @value.setter
    def value(self, value):
        self._view["value"] = value
