import json
import unittest

import responses

import api
from errors import AuthError


FAKE_TOKEN = 'fake_token_1'


class TestTogglBase(unittest.TestCase):
    """ Class to establish utility methods for Test classes. """

    api_token = FAKE_TOKEN
    focus_class = None

    def setUp(self):
        self.toggl = api.Toggl(self.api_token)

    def get_json(self, filename):
        """ Return the JSON data contained in the given filename as a dict. """
        with open('json/{}.json'.format(filename)) as json_file:
            json_dict = json.load(json_file)
            json_file.close()
        return json.dumps(json_dict)

    @property
    def full_url(self):
        return self.toggl.api_url + self.focus_class.uri


class TestToggl(TestTogglBase):

    @responses.activate
    def test_wrong_token(self):
        """ Should raise exception when wrong API token is provided. """
        full_url = self.toggl.api_url + self.toggl.User.uri
        responses.add(responses.GET, full_url, status=403)
        self.assertRaises(AuthError, self.toggl.User.get)
        self.assertEqual(len(responses.calls), 1)


class TestClients(TestTogglBase):
    focus_class = api.Clients

    @responses.activate
    def test_create(self):
        """ Should create a new Client. """
        responses.add(
            responses.POST,
            self.full_url,
            body=self.get_json('client_create'),
            status=200,
            content_type='application/json'
        )

        new_client_data = {"client": {"name": "Very Big Company", "wid": 777}}
        response = self.toggl.Clients.create(new_client_data)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_by_id(self):
        """ Should get a specific Client by ID. """
        client_id = 1239455
        full_url = '{url}/{id}'.format(url=self.full_url, id=client_id)
        responses.add(
            responses.GET,
            full_url,
            body=self.get_json('client_get'),
            status=200,
            content_type='application/json'
        )

        response = self.toggl.Clients.get(id=client_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)


class TestUser(TestTogglBase):
    focus_class = api.User

    @responses.activate
    def test_get(self):
        """ Should successfully establish the client. """
        responses.add(
            responses.GET,
            self.full_url,
            body=self.get_json('user_get'),
            status=200,
            content_type='application/json'
        )

        response = self.toggl.User.get()

        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)


if __name__ == '__main__':
    unittest.main()
