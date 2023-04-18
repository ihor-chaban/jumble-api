import unittest
import json
import requests

class TestRandomWordAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:8000/"

    def test_valid_input(self):
        # Test with a valid input
        endpoint = "random_word/"
        input_word = "hello"
        response = requests.get(self.base_url + endpoint + input_word)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.text, input_word)

    def test_empty_input(self):
        # Test with an empty input
        input_word = ""
        endpoint = "random_word/"
        response = requests.get(self.base_url + endpoint + input_word)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.text)["detail"], "Not Found")

    def test_invalid_endpoint(self):
        # Test with an invalid path
        input_word = "hello"
        invalid_endpoint = "random_word_foo/"
        response = requests.get(self.base_url + invalid_endpoint + input_word)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.text)["detail"], "Not Found")

    def test_with_auth_success(self):
        # Test with successful authentication
        input_word = "hello"
        endpoint = "random_word_with_auth/"
        token = "my-secret-api-key"
        response = requests.get(self.base_url + endpoint + input_word, headers={"Authorization": token})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.text, input_word)

    def test_with_auth_fail(self):
        # Test with failed authentication
        input_word = "hello"
        endpoint = "random_word_with_auth/"
        token = "my-secret-api-key-foo"
        response = requests.get(self.base_url + endpoint + input_word, headers={"Authorization": token})
        self.assertEqual(response.status_code, 401)
        self.assertNotEqual(response.text, input_word)
