import unittest

from starlette.testclient import TestClient

from app import app


class AppTests(unittest.TestCase):
    def test_app_is_created(self):
        self.assertTrue(app is not None)

    def test_health_endpoint(self):
        with TestClient(app) as client:
            response = client.get('/health')
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['status'], 'Healthy')


if __name__ == '__main__':
    unittest.main()
