from unittest import TestCase


class TestPage(TestCase):
    def test_page(self):
        from amis_py.components import Page
        from amis_py.components.form import InputNumber, InputNumberProperties
        from amis_py.simple.form import SimpleForm

        class TestForm(SimpleForm):
            def create(self):
                self.data = {
                    "id": None
                }

            def view(self):
                return {
                    "id": InputNumber(InputNumberProperties(label="id")),
                }

        test_form = TestForm()
        page = Page().add(test_form) view = page.render()
        print(view)
