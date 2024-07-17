import unittest
from app import app

class WeatherAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_weather(self):
        response = self.app.post('/', data=dict(city='Tokyo'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Temperature', response.data)

    def test_history(self):
        response = self.app.get('/api/history')
        self.assertEqual(response.status_code, 200)

    def test_autocomplete(self):
        response = self.app.get('/api/autocomplete', query_string={'query': 'To'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
