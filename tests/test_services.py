import json
import unittest
from http.server import HTTPServer
from threading import Thread
from urllib.request import urlopen

from services.auth.app import Handler as AuthHandler
from services.catalog.app import Handler as CatalogHandler
from services.orders.app import Handler as OrdersHandler
from services.notifications.app import Handler as NotificationsHandler


class ServiceTests(unittest.TestCase):
    def check_endpoint(self, handler, route, expected_service):
        server = HTTPServer(("127.0.0.1", 0), handler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            with urlopen(
                f"http://127.0.0.1:{server.server_port}{route}"
            ) as response:
                data = json.loads(response.read())
                self.assertEqual(response.status, 200)
                self.assertEqual(data["service"], expected_service)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_auth_service(self):
        self.check_endpoint(AuthHandler, "/auth", "auth-service")

    def test_catalog_service(self):
        self.check_endpoint(CatalogHandler, "/products", "catalog-service")

    def test_orders_service(self):
        self.check_endpoint(OrdersHandler, "/orders", "orders-service")

    def test_notifications_service(self):
        self.check_endpoint(
            NotificationsHandler,
            "/notifications",
            "notifications-service",
        )


if __name__ == "__main__":
    unittest.main()
