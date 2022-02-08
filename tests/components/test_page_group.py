from unittest import TestCase


class TestPageGroup(TestCase):
    def test_page_group(self):
        from amis_py.components import (
            Page, PageGroup, PageProperties, PageGroupProperties)
        from amis_py.components.form import InputNumber, InputNumberProperties
        from amis_py.simple.form import SimpleForm
    
        class TestForm(SimpleForm):
            def create(self):
                self.data = {
                    "id": 1
                }

            def view(self):
                return {
                    "id": InputNumber(InputNumberProperties(label="id")),
                }

        test_form = TestForm()
        page1 = Page(PageProperties(title="page1")).add(test_form)
        page2 = Page(PageProperties(title="page2")).add(test_form)
        page_group = PageGroup(PageGroupProperties(title="group1"))
        page_group.add(page1)
        page_group.add(page2)
        view = page_group.render()
        assert view == {
            "children": [
                {
                    "label": "page1",
                    "schema": {
                        "type": "page",
                        "title": "page1",
                        "body": [{
                            "type": "form",
                            "api": "",
                            "body": [{
                                "type": "input-number",
                                "label": "id",
                                "name": "id",
                                "value": 1
                            }]
                        }]
                    }
                },
                {
                    "label": "page2",
                    "schema": {
                        "type": "page",
                        "title": "page2",
                        "body": [{
                            "type": "form",
                            "api": "",
                            "body": [{
                                "type": "input-number",
                                "label": "id",
                                "name": "id",
                                "value": 1
                            }]
                        }]
                    }
                 }
            ],
            "title": "group1",
        }
