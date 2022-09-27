import json
from unittest.mock import patch, Mock

from django.test import TestCase


# Create your tests here.
class ForecastAPITests(TestCase):
    @patch('weather.api.views.requests.get')
    def test_success_api_response(self, mock_requests):
        # Mock request data
        mock_requests.return_value = mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"forecast":{
            "forecastday":[
                {"day":{"maxtemp_c":14.6,"mintemp_c":8.6, "avgtemp_c":11.4}},
                {"day":{"maxtemp_c":45.8,"mintemp_c":8.3, "avgtemp_c":4.2}},
                {"day":{"maxtemp_c":0.5,"mintemp_c":2.7, "avgtemp_c":28.9}}
            ]
        }
        }

        response = self.client.get('/api/location/nairobi/?days=2')
        self.assertEqual(response.status_code, 200)

        # Check response contains temperature calculations
        self.assertContains(response, "maximum")
        self.assertContains(response, "minimum")
        self.assertContains(response, "average")
        self.assertContains(response, "median")

    def test_invalid_request_parameters(self):
        # request with wrong city
        response = self.client.get('/api/location/3455/')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'"City parameter must be a string"')

        # Request with wrong number of days
        response = self.client.get('/api/location/nairobi/?days=38')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'"Days must be greater than 0 and less than 15"')