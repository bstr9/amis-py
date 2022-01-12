class BaseComponent:
    __type = "base"
    __view = {}

    def view(self):
        return {}

    def create(self):
        self.data = {}

    def render(self):
        return {}
