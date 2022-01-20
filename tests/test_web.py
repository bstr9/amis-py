import threading
import requests

from unittest import TestCase
from amis_py.web_server import App


class TestWebResponse(TestCase):
    def test_url_regex(self):
        port = 1111
        app = App(port=port)

        user_url = "/api/v1/user/<id>"
        user_name_url = "/api/v1/user/<id>/name"
        user_update_name_url = "/api/v1/user/<id>/name/<name>"

        def user_test(id):
            return "user" + id

        def user_name_test(id):
            return id

        def user_update_name(id, name):
            return "user" + id + name

        app.add_route(user_url, user_test)
        app.add_route(user_name_url, user_name_test)
        app.add_route(user_update_name_url, user_update_name)

        threading.Thread(
            target=app.run, args=(), daemon=True).start()

        res = requests.get(
            "http://localhost:{}{}".format(
                port, user_url.replace("<id>", "1")))
        assert res.text == "user1"
        res = requests.get(
            "http://localhost:{}{}".format(
                port, user_name_url.replace("<id>", "2")))
        assert res.text == "2"
        res = requests.post(
            "http://localhost:{}{}".format(
                port,
                user_update_name_url.replace(
                    "<id>", "3").replace("<name>", "test")
            )
        )
        assert res.text == "user3test"
        app.stop()
