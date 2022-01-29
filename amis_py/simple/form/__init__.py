from amis_py.components import Form
from amis_py.exceptions import TypeInvalidError
from logging import getLogger


class SimpleForm(Form):
    def __init__(self):
        # use self.create() to generate default dataset
        super().__init__()
        self._view = {
            "type": "form",
            "api": "",
            "body": []
        }

        self.create()
        if not isinstance(self.data, dict):
            raise TypeInvalidError(
                "component Form can't accept data with type"
                "{}".format(type(self.data)))

        # use self.view() to get default view style
        view = self.view()
        if not isinstance(view, dict):
            raise TypeInvalidError(
                "component Form can't accept view with type"
                "{}".format(type(view)))

        # fulfill the default value to view
        for default_k, default_v in self.data.items():
            hitted = False
            for view_k, view_v in view.items():
                if view_k == default_k:
                    hitted = True
                    if not hasattr(view_v, "render"):
                        raise TypeInvalidError(
                            "set invalid component {} as view".format(
                                view_v.__class__.__name__
                            )
                        )
                    view_v.name = view_k
                    self._view.get("body").append(view_v.render())
            if not hitted:
                getLogger().warning(f"{default_k} was setted in default data,"
                                    "but not setted in view")

    def render(self):
        return self._view

