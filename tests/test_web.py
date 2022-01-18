import threading
import requests

from unittest import TestCase
from amis_py.web_server import App


class TestWebResponse(TestCase):
    def test_url_regex(self):
        port = 1111
        app = App(port=port)
        t = threading.Thread(
            target=app.run, args=(), daemon=True).start()

        user_url = "/api/v1/user/<id>"
        user_name_url = "/api/v1/user/<id>/name"

        def user_test(id):
            assert id == '1'
            return 1

        def user_name_test(id):
            assert id == "1"
            return "test"

        app.add_route(user_url, user_test)
        app.add_route(user_name_url, user_name_test)

        requests.get(
            "http://localhost:{}{}".format(port, user_url))
        requests.get(
            "http://localhost:{}{}".format(port, user_name_url))

        app.stop()
        t.join()

    def test_return_json(self):
        port = 1111
        app = App(port=port)
        t = threading.Thread(
            target=app.run, args=(), daemon=True).start()

        user_info_url = "/api/v1/user/<id>/info"

        def user_info(id):
            assert id == "1"
            return {"name": "test", "id": "1"}

        app.add_route(user_info_url, user_info)
        res = requests.get(
            "http://localhost:{}{}".format(port, user_info_url))
        assert res.json() == {"name": "test", "id": "1"}

        app.stop()
        t.join()
