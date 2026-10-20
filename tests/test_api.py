import json
import unittest
from http.server import HTTPServer
from threading import Thread
from urllib.request import urlopen
from urllib.error import HTTPError

from services.api.app import Handler


class APITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_health(self):
        with urlopen(f"{self.base_url}/health") as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(
                json.loads(response.read()),
                {"status": "healthy"}
            )

    def test_root(self):
        with urlopen(self.base_url + "/") as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(
                json.loads(response.read())["service"],
                "devsecops-api"
            )

    def test_unknown_route(self):
        with self.assertRaises(HTTPError) as error:
            urlopen(self.base_url + "/unknown")
        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
