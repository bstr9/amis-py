from amis_py.utils import is_default


class BaseComponent:
    __type = "base"
    __view = {}

    def view(self):
        return {}

    def create(self):
        self.data = {}

    def render(self):
        return {}

    def _set_default(self, key, value, default=None):
        if not is_default(value, default):
            self.__view.update({key, value})
