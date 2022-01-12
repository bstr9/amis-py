# amis-py

## Examples

DataSource -> Model -> ViewModel -> View(amis json)

```

from amis-py import property
from amis-py import Page

class Config:
    def __init__(self, path):
        self.path = path
        self.load()

    def save(self):
        json.dump(self.config, path)

    def load(self):
        self.config = json.load(self.path)

    def update(self, k, v):
        self.config.update({k: v})
        self.save()

    def delete(self, k):
        del self.config.get(k)

    def get(self, k):
        return self.config.get(k)


# ViewModel
class ConfigModel:
    def __init__(self, config):
        self.config = config 

    @property
    def a(self):
        return self.config.get("a")

    @a.setter
    def set_a(self, value):
        self.config.update("a", value})

    @a.deleter
    def delete_a(self):
        self.config.delete("a")


# View
class ConfigPage(Page):
    def __init__(self, model):
        self.model = model
        self.template = [
            Header(bind={"a": self.model.a}, style="???"),
            Card([
                Title(bind={"a": self.model.a}),
                Table(bind={"users": self.model.users}, delete=True, edit=True),
            ])
        ]
```
