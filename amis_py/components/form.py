from .base import BaseComponent
from logging import getLogger


class Form(BaseComponent):
    pass


class FormItemProperties:
    __defaults = {
        "label": [str, ""],
        "description": [str, ""],
        "inline": [bool, None],
        "disabled": [bool, None],
        "visible": [bool, None],
        "required": [bool, None],
        "validations": [str, ""]
    }

    def __init__(self, **kwargs):
        self.params = {}
        for k, v in kwargs.items():
            if k in self.__default:
                if type(v) is self.__default.get(k)[0]:
                    self.params.update({k: v})
                else:
                    getLogger().warning(
                        "field {} not must be type:{}, current type:{},"
                        "ignore the field {}".format(
                            k, self.__default.get(k), type(v), k
                        )
                    )
                    self.params.update({k: self.__default.get(k)[1]})

    def get(self, prop):
        return self.__default.get(prop)


class FormItem(BaseComponent):
    __type = "form-item"

    def __init__(
        self,
        props: FormItemProperties
    ):
        self.__view = {
            "type": self.__type,
            "name": "",
            "label": self.__default.get("label"),
        }


class InputTextProperties(FormItemProperties):
    __defaults = FormItemProperties.__defaults

    def __new__(cls, *args, **kwargs):
        defaults = {
            "min_value": [int, None]
        }
        instance = super().__new__(cls)
        instance.__default.update(defaults)


class InputText(BaseComponent):
    def __init__(self):
        pass


class InputNumber(BaseComponent):
    """
    doc:
    """
    __type = "input-number"

    def __init__(
        self, label="", min_value=None, max_value=None, step=None,
        precision=None, show_steps=None, prefix="",
        suffix="", kilobit_separator=None,
    ):
        self.__view = {
            "type": self.__type,
            "name": "",
            "label": label,
        }
        self._set_default("min", min_value)
        self._set_default("max", max_value)
        self._set_default("step", step)
        self._set_default("precision", precision)
        self._set_default("showSteps", show_steps)
        self._set_default("prefix", prefix, "")
        self._set_default("suffix", suffix, "")
        self._set_default("kilobitSeparator", kilobit_separator)

    @property
    def name(self):
        return self.__view.get("name")

    @name.setter
    def set_name(self, name):
        self.__view["name"] = name
        if self.__view.get("label") == "":
            self.__view["label"] = name

    @property
    def value(self):
        return self.__view.get("value")

    @value.setter
    def set_value(self, value):
        self.__view["name"] = value

    def render(self):
        return self.__view

    def trans_default(self, value):
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return value
        if isinstance(value, str):
            try:
                if self.precision is not None:
                    if self.precision > 0:
                        return float(value)
                    else:
                        return int(value)
            except Exception:
                return None
        else:
            return None


class InputPassword(BaseComponent):
    pass


class InputEmail(BaseComponent):
    pass
