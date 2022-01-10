from amis_py.simple.form import (
    SimpleForm, TextItem, EmailItem,
    NumberItem, PasswordItem, TableItem,
    Submit, Select, Static, StaticDatetime, Combo,
    Switch
)
from amis_py import props


class UserForm(SimpleForm):
    def __init__(self):
        self.width = 500
        self.height = 100
        self.title = "user"

    def load(self):
        self.data = {"id": 1, "name": "test"}

    def save(self):
        pass

    @props
    def name(self):
        return self.data.get("name")

    @name.view
    def name_item(self):
        return TextItem()

    @name.setter
    def set_name(self, name):
        self.data.update({"name": name})

    @props
    def id(self):
        return self.data.get("id")

    @id.setter
    def set_id(self, id):
        self.data.update({"id": id})

    @id.view
    def id_item(self):
        return NumberItem()
