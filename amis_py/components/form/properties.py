from logging import getLogger
from amis_py.utils import is_default


class _Prop:
    def __init__(self, name, prop_type, default, rename=""):
        self._type = prop_type
        self._default = default
        self._name = name
        if rename != "":
            self._rename = rename
        else:
            self._rename = name

    def get_type(self):
        return self._type

    def get_default(self):
        return self._default

    def get_name(self):
        return self._name

    def get_real_name(self):
        return self._rename

    def __str__(self):
        return f"field:{self._rename}:{self._type.__name__}:{self._default}"


class FormItemProperties:
    __defaults = [
        _Prop("name", str, ""),
        _Prop("label", str, ""),
        _Prop("description", str, ""),
        _Prop("inline", bool, None),
        _Prop("disable", bool, None),
        _Prop("visible", bool, None),
        _Prop("required", bool, None),
        _Prop("validations", str, ""),
        _Prop("value", str, None)
    ]

    def __init__(self, **kwargs):
        self.properties = {}
        for k, v in kwargs.items():
            if self.has_default(k):
                prop = self.get_default(k)
                if isinstance(v, prop.get_type()):
                    if not is_default(v, prop.get_default):
                        self.properties.update({prop.get_name(): v})
                else:
                    getLogger().warning(
                        "field {field} not must be type:{_type} "
                        "current type:{cur_type},"
                        " ignore the field {field}={value}".format(
                            field=k,
                            value=v,
                            _type=prop.get_type().__name__,
                            cur_type=type(v).__name__),
                    )

    @classmethod
    def update_defaults(cls, props: [_Prop]):
        extended_props = []
        for prop in props:
            hitted = False
            for index, ori_prop in enumerate(cls.__defaults):
                if prop.get_name() == ori_prop.get_name():
                    cls.__defaults[index] = prop
            if not hitted:
                extended_props.append(prop)
        cls.__defaults.extend(extended_props)

    @classmethod
    def has_default(cls, name):
        for prop in cls.__defaults:
            if name == prop.get_name():
                return True
        return False

    def get(self, prop):
        return self.properties.get(prop)

    @classmethod
    def get_default(cls, name):
        for prop in cls.__defaults:
            if name == prop.get_name():
                return prop
        return None

    @property
    def defaults(self):
        return self.__defaults
