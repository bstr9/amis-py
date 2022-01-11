from amis_py.components import Form
from amis_py.exceptions import TypeInvalidError


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
        for k, v in view:
            for default_k, default_v in self.data.items():
                if k == default_k:
                    self.__view.get("body").append(v.render())

    def create(self):
        self.data = {}

    def view(self):
        return {}

    def render(self):
        return self.__view
