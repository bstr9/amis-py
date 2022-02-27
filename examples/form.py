import sys
import os
sys.path.append(os.path.abspath(".."))

from amis_py.components.form import (
    InputNumber, InputNumberProperties,
)
from amis_py.simple.form import SimpleForm as Form
from amis_py.components import Page
from amis_py import App


class UserForm(Form):
    def create(self):
        user = {"id": 1}
        self.data = {
            "id": user.get("id"),
        }

    def view(self):
        return {
            "id": InputNumber(InputNumberProperties(label="id")),
        }


if __name__ == "__main__":
    app = App(view=True)
    app.add(Page().add(UserForm()))
    app.run()
