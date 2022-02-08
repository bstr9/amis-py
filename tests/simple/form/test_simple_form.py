from unittest import TestCase
from tests.exceptions import UnitTestException


class TestSimpleForm(TestCase):
    def test_default_data(self):
        from amis_py.simple.form import SimpleForm
        from amis_py.components.form import InputNumber, InputNumberProperties

        class TestForm(SimpleForm):
            def create(self):
                self.data = {
                    "id": 1,
                }

            def view(self):
                return {
                    "id": InputNumber(InputNumberProperties(label="id")),
                }

        test_form = TestForm()
        view = test_form.render()
        for item in view.get("body"):
            label = item.get("label")
            if label == "id":
                assert item == {
                    "type": "input-number",
                    "label": "id",
                    "name": "id",
                    "value": 1
                }
            else:
                raise UnitTestException(
                    f"invalid label {label} in TestSimpleForm view")
