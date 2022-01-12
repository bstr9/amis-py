# amis-py

## Examples

DataSource -> Model -> ViewModel -> View(amis json)

```
from amis_py.components.form import (
    Form,
    InputNumber, InputNumberProperties,
    InputText, InputTextProperties,
    InputEmail, InputEmailProperties
)
from amis_py.components import Page
from amis_py import App

import requests


class User:
    def __init__(self):
        """
            self.user = {
                "id": 1,
                "name": "test",
                "email": "test@mock.com"
            }
        """
        self.user = requests.get("http://mock/user/1").json()
    
    def get(self, key):
        return self.user.get(key)


class UserForm(Form):
    def create(self):
        user = User()
        self.data = {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email")
        }

    def view(self):
        return {
            "id": InputNumber(InputNumberProperties(label="id")),
            "name": InputText(
                InputTextProperties(label="name", name="username")),
            "email": InputEmail(
                InputEmailProperties(label="email"))
        }

if __name__ == "__main__"
    app = App()
    app.add(Page().add(UserForm()))
    app.run()
```
