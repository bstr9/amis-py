from logging import getLogger
from amis_py.utils import is_default, get_random_hash


class Prop:
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


class Properties:
    def __init__(self):
        self.defaults = []
        self.properties = {}

    def update_properties(self, **kwargs):
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

    def update_defaults(self, props: [Prop]):
        extended_props = []
        for prop in props:
            hitted = False
            for index, ori_prop in enumerate(self.defaults):
                if prop.get_name() == ori_prop.get_name():
                    self.defaults[index] = prop
            if not hitted:
                extended_props.append(prop)
        self.defaults.extend(extended_props)

    def has_default(self, name):
        for prop in self.defaults:
            if name == prop.get_name():
                return True
        return False

    def get(self, prop):
        return self.properties.get(prop)

    def get_default(self, name):
        for prop in self.defaults:
            if name == prop.get_name():
                return prop
        return None


class BaseComponent:
    def __init__(self, props):
        self._type = "base"
        self._view = {}
        self.props = props

    def update(self):
        # use update function to update model dataset
        return

    def view(self):
        # the view function is used to set sub components
        return {}

    def create(self):
        # use create function to generate default dataset
        self.data = {}

    def render(self):
        # the render function is the hook for amis_py.components.BaseComponent
        return self._view
    
    @property
    def route(self):
        # the route function returns the component's route url
        return "/{}/{}".format(self._type, hash(self))
