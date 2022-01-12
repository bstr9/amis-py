from .form_item import FormItem
from .properties import FormItemProperties, _Prop


class InputNumberProperties(FormItemProperties):
    def __new__(cls, *args, **kwargs):
        defaults = [
            _Prop("min_value", int, None, "min"),
            _Prop("max_value", int, None, "max"),
            _Prop("step", int, None),
            _Prop("precision", float, None),
            _Prop("show_steps", int, None, "showSteps"),
            _Prop("prefix", str, ""),
            _Prop("suffix", str, ""),
            _Prop("kilobit_separator", int, None, "kilobitSeparator"),
            _Prop("unit_options", list, None, "unitOptions"),
            _Prop("value", int, None)
        ]
        instance = super().__new__(cls)
        instance.__defaults = instance.update_defaults(defaults)
        return instance


class InputNumber(FormItem):
    """
    doc:
    """
    __type = "input-number"

    def __init__(
        self, props: InputNumberProperties = InputNumberProperties()
    ):
        self.__view = {
            "type": self.__type,
        }
        self.__view.update(props.properties)
        if not props.get("name"):
            self.__view["name"] = props.get("label")

    @property
    def name(self):
        return self.__view.get("name")

    @name.setter
    def name(self, name):
        self.__view["name"] = name
        if self.__view.get("label") == "":
            self.__view["label"] = name

    @property
    def value(self):
        return self.__view.get("value")

    @value.setter
    def value(self, value):
        self.__view["name"] = value

    def render(self):
        return self.__view
