from unittest import TestCase
from tests.exceptions import UnitTestException


class TestSimpleForm(TestCase):
    def test_default_data(self):
        from amis_py.simple.form import SimpleForm
        from amis_py.components.form import (
            InputNumber, InputText, InputPassword, InputEmail)

        class TestForm(SimpleForm):
            def create(self):
                self.data = {
                    "id": None,
                    "name": "",
                    "password": "",
                    "email": ""
                }

            def view(self):
                return {
                    "id": InputNumber(),
                    "name": InputText(),
                    "password": InputPassword(),
                    "email": InputEmail()
                }

        test_form = TestForm()
        view = test_form.render()
        for item in view.get("body"):
            label = item.get("label")
            if label == "id":
                assert item == {}
            elif label == "name":
                assert item == {}
            elif label == "password":
                assert item == {}
            elif label == "email":
                assert item == {}
            else:
                raise UnitTestException(
                    f"invalid label {label} in TestSimpleForm view")
