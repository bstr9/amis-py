from amis_py.components import Form
from amis_py.exceptions import TypeInvalidError
from logging import getLogger


class SimpleForm(Form):
    __view = {
        "type": "form",
        "api": "",
        "body": []
    }

    def __init__(self):
        self.data = {}
        self.create()
        view = self.view()
        if not isinstance(self.data, dict):
            raise TypeInvalidError(
                "component Form can't accept data with type"
                "{}".format(type(self.data)))
        if not isinstance(view, dict):
            raise TypeInvalidError(
                "component Form can't accept view with type"
                "{}".format(type(view)))
        for default_k, default_v in self.data.items():
            hitted = False
            for k, v in view.items():
                if k == default_k:
                    hitted = True
                    if not hasattr(v, "render"):
                        raise TypeInvalidError(
                            "set invalid component {} as view".format(
                                v.__class__.__name__
                            )
                        )
                    v.name = k
                    self.__view.get("body").append(v.render())
            if not hitted:
                getLogger().warning(
                    "{} was setted in default data,"
                    "but not setted in view".format(default_k))

    def create(self):
        self.data = {}

    def view(self):
        return {}

    def render(self):
        return self.__view
