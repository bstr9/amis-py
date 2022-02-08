from unittest import TestCase


class TestApp(TestCase):
    def test_app(self):
        from amis_py.components import (
            App, Page, PageGroup
        )
        from amis_py.components.form import InputNumber, InputNumberProperties
        from amis_py.simple.form import SimpleForm

        class TestForm(SimpleForm):
            def create(self):
                self.data = {
                    "id": 1
                }
