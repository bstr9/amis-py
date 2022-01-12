# amis_py.simple.form.SimpleForm

## Example
```
from sqlalchemy import Model
from sqlalchemy.fields import StringField


class User(Model):
    username = StringField(name="username")
    password = StringField(name="password")


from amis_py.simple.form import SimpleForm, api, init_api
from amis_py.component import Page
from amis_py import app 

class UserForm(SimpleForm):

    @init_api
    def init(self):
        return {
            "username": "",
            "password": ""
        }

    def create(self):
        self.data = {
            "username": "",
            "password": ""
        }

    def view(self):
        return {
            "username": InputText(),
            "password": InputPassword()
        }

    @api
    def add_user(self, username, password):
        user = User(username=username, password=password).commit()


class MainPage(Page):
    def create(self):
        self.title = "home"

    def view(self):
        return {
            "user_form": UserForm()
        } 


if __name__ == "__main__":
    app.add(MainPage())
    app.run()
```
